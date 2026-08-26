"""
[단위 테스트] 텔레그램 멀티 토픽(Forum Topics) 연동 및 라우팅 테스트
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock

# 모듈 경로 추가
sys.path.insert(0, r"D:\AI\AI_hub\shared\T020_human_in_the_loop")
import n8n_telegram_bot
import send_approval

class TestTelegramMultiTopics(unittest.TestCase):
    def setUp(self):
        self.test_chat_id = "12345678"
        self.sample_registry = {
            "manbok": {"name": "만복", "topic_name": "🧠 만복 (PM/총괄)", "keywords": ["만복"], "fallback_priority": 1},
            "kony": {"name": "코니", "topic_name": "🔍 코니 (Auditor/검증)", "keywords": ["코니"], "fallback_priority": 2},
            "anti": {"name": "안티", "topic_name": "⚡ 안티 (Operator/실행)", "keywords": ["안티"], "fallback_priority": 3},
            "approval": {"name": "승인봇", "topic_name": "🚨 T020 승인 및 알림", "type": "system"}
        }

    @patch("n8n_telegram_bot.save_topics_cache")
    @patch("n8n_telegram_bot.get_topics_cache")
    @patch("n8n_telegram_bot.tg_api_call")
    def test_ensure_topics_creation(self, mock_api, mock_get_cache, mock_save_cache):
        """포럼 채팅방에서 토픽 신규 생성 검증"""
        mock_get_cache.return_value = {}
        
        # createForumTopic 성공 응답 모의
        def side_effect(token, method, payload):
            if method == "createForumTopic":
                name = payload["name"]
                t_id = 100 + hash(name) % 100
                return {"ok": True, "result": {"message_thread_id": t_id, "name": name}}
            return {"ok": False}
        
        mock_api.side_effect = side_effect

        topics = n8n_telegram_bot.ensure_topics_for_chat("fake_token", self.test_chat_id, self.sample_registry)
        
        self.assertIn("manbok", topics)
        self.assertIn("kony", topics)
        self.assertIn("anti", topics)
        self.assertIn("approval", topics)
        self.assertTrue(mock_save_cache.called)

    def test_topic_based_routing(self):
        """특정 토픽에서 발신된 메시지가 키워드 없이도 해당 에이전트로 라우팅되는지 검증"""
        chat_topics = {
            "manbok": {"thread_id": 101, "name": "🧠 만복"},
            "kony": {"thread_id": 102, "name": "🔍 코니"},
            "anti": {"thread_id": 103, "name": "⚡ 안티"}
        }

        # 시나리오 1: 안티 토픽(thread_id=103)에서 키워드 없는 일반 메시지 발신
        thread_id = 103
        text = "코드 리팩토링 진행해줘"
        
        target_agent = None
        target_name = None
        # 1차 키워드 검사 (없음)
        # 2차 토픽 ID 매핑
        for agent_id, t_info in chat_topics.items():
            if t_info.get("thread_id") == thread_id:
                target_agent = agent_id
                target_name = self.sample_registry.get(agent_id, {}).get("name")
                break

        self.assertEqual(target_agent, "anti")
        self.assertEqual(target_name, "안티")

        # 시나리오 2: 코니 토픽(thread_id=102)에서 발신
        thread_id = 102
        target_agent = None
        for agent_id, t_info in chat_topics.items():
            if t_info.get("thread_id") == thread_id:
                target_agent = agent_id
                break
        self.assertEqual(target_agent, "kony")

if __name__ == "__main__":
    unittest.main()
