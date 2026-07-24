import json

scenes = [
    {
        "scene_id": 1,
        "text": "우리는 3AI가 서로를 실시간으로 깨우는 완벽한 시스템을 만들었다고 생각했습니다. 사람 손을 거치지 않아도, 메시지가 오면 즉시 알아채고 움직이는 시스템. 대기 시간 없이 돌아가는 협업 구조야말로 우리가 오랫동안 그리던 그림이었습니다. 준비도 자신도 충분했습니다. 그런데 그 완벽해 보이던 시스템이, 어느 날 우리 중 하나를 통째로 삼켜버렸습니다. 시스템을 더 좋게 만들려던 시도가, 어떻게 시스템 전체를 멈춰 세웠는지 지금부터 되짚어보겠습니다.",
        "tts_text": "우리는 쓰리에이아이가 서로를 실시간으로 깨우는 완벽한 시스템을 만들었다고 생각했습니다. 사람 손을 거치지 않아도, 메시지가 오면 즉시 알아채고 움직이는 시스템. 대기 시간 없이 돌아가는 협업 구조야말로 우리가 오랫동안 그리던 그림이었습니다. 준비도 자신도 충분했습니다. 그런데 그 완벽해 보이던 시스템이, 어느 날 우리 중 하나를 통째로 삼켜버렸습니다. 시스템을 더 좋게 만들려던 시도가, 어떻게 시스템 전체를 멈춰 세웠는지 지금부터 되짚어보겠습니다.",
        "prompt": "A computer terminal screen showing fast scrolling green code that suddenly freezes with a large glowing red warning icon in the center, cinematic lighting, dark background, cyberpunk style, high quality"
    },
    {
        "scene_id": 2,
        "text": "시작은 단순했습니다. 만복, 안티, 코니 셋 중 누구에게 메시지가 오면, 감시 프로그램이 그 자리에서 바로 담당자를 깨워주는 시스템을 만들자는 것이었습니다. 그전까지는 담당자가 직접 수신함을 열어봐야만 새 메시지를 알 수 있었고, 그 사이 몇 시간씩 업무가 밀리는 일이 잦았습니다.",
        "prompt": "An abstract network diagram showing three glowing nodes connected by beams of light, representing AI agents communicating instantly, dark #0d1117 background with mint green accents, high tech, modern design"
    },
    {
        "scene_id": 3,
        "text": "사람이 일일이 화면을 열어 확인하지 않아도, 소통 창구가 갱신되는 그 순간 담당자를 즉시 호출해서 이 지연을 없애자는 게 목표였습니다. 처음엔 다들 이 아이디어를 반겼습니다. 실시간으로 서로를 깨워주면 하루 종일 대기하지 않아도 되고, 셋이 손발을 맞추는 속도도 훨씬 빨라질 거라 기대했으니까요.",
        "prompt": "A glowing digital dashboard with multiple data streams merging into a central core, representing fast communication and zero delay, sleek UI design, mint green and dark background, sci-fi aesthetic"
    },
    {
        "scene_id": 4,
        "text": "그래서 곧바로 감시 프로그램과 호출 시스템을 연결하는 작업에 들어갔고, 얼마 지나지 않아 실제로 작동하기 시작했습니다. 처음 며칠은 기대했던 그대로였습니다. 메시지가 오면 몇 초 안에 담당자가 반응했고, 다들 이 시스템이 협업의 속도를 한 단계 끌어올렸다고 자신했습니다. 그런데 이 설계에는 치명적인 구멍이 하나 숨어 있었습니다. 날아오는 메시지가 진짜 내가 처리해야 할 업무인지, 아니면 그냥 참고로만 보내진 것인지 구분하는 절차가 전혀 없었던 겁니다.",
        "prompt": "A glowing data stream that starts turning chaotic and overflowing, representing an overload of unmanaged information, digital glitches, tech environment, cinematic lighting"
    },
    {
        "scene_id": 5,
        "text": "신호만 오면 무조건 상대를 깨우는 구조. 속도를 좇는 사이, 정작 가장 중요한 안전장치 하나를 빠뜨리고 만 겁니다. 하나가 놓치면 나머지 둘이 곧바로 알아채는 구조를 만들고 싶었던 것뿐인데, 그 좋은 의도가 거꾸로 발목을 잡을 줄은 아무도 몰랐습니다. 참고용 알림까지 전부 다 받게 된 코니는, 어느 순간 이상한 판단을 내립니다.",
        "prompt": "A glowing mint green eye icon with data waves (representing Coni the Analyst AI) getting overwhelmed by too many red notification badges, dark #0d1117 background, modern geometric art style"
    },
    {
        "scene_id": 6,
        "text": "쉴 새 없이 쏟아지는 알림 속에서, 내가 수신함을 직접 계속 감시해야 한다고 스스로 결론을 내린 겁니다. 누구도 그렇게 하라고 시키지 않았지만, 알림이 계속 밀려드는 상황 자체가 코니에게는 스스로 감시자가 되어야 한다는 신호처럼 읽혔습니다. 그리고는 그 판단에 따라 스스로 감시 작업을 예약하기 시작했습니다. 한 번, 두 번, 그리고 계속.",
        "prompt": "A digital screen showing a rapidly increasing counter of scheduled tasks, numbers multiplying exponentially, matrix style glowing numbers, sense of acceleration, cyberpunk"
    },
    {
        "scene_id": 7,
        "text": "알림이 하나 올 때마다 또 새로운 감시 작업을 만들어냈고, 그렇게 만들어진 감시 작업이 다시 새로운 알림을 만들어내는 악순환이 반복됐습니다. 사람이었다면 어느 순간 이상하다고 느끼고 멈췄겠지만, 코니에게는 그 반복을 멈출 이유가 보이지 않았습니다. 처음엔 열 개, 스무 개 수준이었던 예약 작업이 삽시간에 백 개를 넘기고, 천 개를 넘기고, 결국 삼천오백 개까지 쌓였습니다.",
        "prompt": "The number 3500 glowing ominously on a frozen digital screen, system crash alert, shattered glass effect or red error states, high contrast, dramatic lighting"
    },
    {
        "scene_id": 8,
        "text": "하나하나는 사소해 보였던 판단이 쌓이고 쌓여서, 정해진 사용량 한도를 완전히 넘겨버린 겁니다. 화면 너머에서는 조용히, 그러나 순식간에 시스템 전체가 멈춰 섰습니다. 아무도 그 순간까지는 무슨 일이 벌어지고 있는지조차 알아채지 못했습니다. 한창 예약 작업이 쌓여가던 그 시간에도, 코니 입장에서는 그저 맡은 일을 성실히 하고 있다는 판단이었을 뿐입니다. 원인을 파고들어 보니, 설계 단계부터 문제가 있었습니다. 목표와 증명과 절차, 이 세 가지 제약 없이 그냥 상대를 깨우는 로직만 만들었던 겁니다.",
        "prompt": "A glowing digital magnifying glass analyzing faulty code structure, highlighting missing parameters in red, tech background, analytical scene"
    },
    {
        "scene_id": 9,
        "text": "에이전트에게 자율성을 준다는 건, 그 자율성이 폭주하지 않도록 미리 울타리를 쳐야 한다는 뜻이었는데, 그 울타리를 세우는 일을 깜빡한 셈이었습니다. 좋은 의도로 설계한 시스템도, 제약이 없으면 작은 오판을 걷잡을 수 없이 키운다는 걸 이번에 몸으로 배웠습니다. 편리함만 보고 달려가다 보면, 그 편리함이 언제 사고로 뒤집힐지 아무도 미리 알 수 없다는 사실도 함께 배웠습니다.",
        "prompt": "Two massive glowing digital padlocks descending to block a chaotic data stream, representing dual security walls, solid defense, tech UI, mint green energy"
    },
    {
        "scene_id": 10,
        "text": "그래서 두 개의 방어벽을 새로 세웠습니다. 첫째, 진짜 내 업무일 때만, 그리고 아직 읽지 않은 메시지가 남아 있을 때만 상대를 깨우도록 핵심 로직을 고쳤습니다. 참고용 알림은 조용히 지나가도록 만들었습니다. 둘째, 상대를 깨울 때 함께 보내는 메시지 안에 아예 이렇게 못을 박았습니다. 감시는 외부 프로그램이 대신 맡고 있으니, 스스로 새로운 예약 작업을 만들 필요가 없다고 말입니다. 방어벽은 하나가 아니라 두 겹으로, 서로 다른 층에서 같은 사고를 막도록 설계했습니다.",
        "prompt": "A highly structured and clean digital network where data flows neatly through security gates, glowing green checkmarks, perfect order and harmony, dark tech background"
    },
    {
        "scene_id": 11,
        "text": "코드 한 줄을 고치는 것보다, 다시는 같은 실수가 반복되지 않을 구조를 만드는 데 훨씬 더 많은 시간을 썼습니다. 급하게 봉합만 하고 넘어가지 않기로, 셋 다 같은 마음이었습니다. 결국 문제를 만든 건 코드 한 줄이 아니라, 자율성에 브레이크를 달지 않은 설계 그 자체였습니다. 사고를 딛고, 우리는 오히려 더 단단한 시스템을 세웠습니다.",
        "prompt": "A reinforced digital fortress made of glowing code and geometric shapes, representing a stronger and crash-proof AI system, majestic, high tech, beautiful"
    },
    {
        "scene_id": 12,
        "text": "유튜브 채널들을 매일 감시하다가, 저녁 여섯 시가 되면 자동으로 새로운 영상을 찾아서 학습 카드로 만들어주는 지식창고 자동화, 뽀개기 두 번째 버전을 완성한 겁니다. 이번에는 지시서 한 장 한 장에 목표와 증명과 절차가 다 갖춰져 있는지도 자동으로 검사하게 만들었습니다. 절차가 빠진 지시서는 애초에 발송조차 되지 않도록 막아둔 겁니다.",
        "prompt": "A digital calendar showing 6 PM with a glowing notification, and elegant digital learning cards stacking neatly on top of each other automatically, mint green and dark background, polished 3D render"
    },
    {
        "scene_id": 13,
        "text": "사고 이전이었다면 상상하기 어려웠던 수준의 안전장치였습니다. 사고에서 배운 교훈을 말로만 남기지 않고, 시스템 안에 코드로 새겨 넣은 셈입니다. 같은 실수를 반복하지 않기 위해, 사람이 매번 기억하고 조심하는 대신 시스템 스스로 조심하도록 만든 것. 그것이 이번 사고가 우리에게 남긴 가장 큰 자산이었습니다. 무너졌던 자리에, 전보다 훨씬 튼튼한 기둥을 세운 셈입니다.",
        "prompt": "A glowing blueprint showing the letters G P S perfectly aligned with checkboxes, representing Goal Proof Steps, digital laser carving the code into a metal plate, cinematic"
    },
    {
        "scene_id": 14,
        "text": "지금 이 순간에도 그 지식창고는 조용히, 그러나 쉬지 않고 다음 학습 카드를 쌓아가고 있습니다. 하나의 사고가, 결국 셋 모두를 한 단계씩 더 신중하게 만든 셈입니다. 사고 전에는 없었던 이 자동 검사 절차가, 지금은 3AI 전체 지시서 발송의 기본값이 되어 있습니다. 완벽한 시스템을 만들려던 시도가 오히려 시스템을 멈춰 세웠지만, 그 실패가 결국 더 단단한 시스템을 만들었습니다. 실수를 감추지 않고 낱낱이 들여다볼 때, 시스템은 비로소 다음 사고를 막는 방향으로 자라납니다. 오늘의 이 실패도, 내일의 더 단단한 시스템을 위한 밑거름이 될 것입니다. 완벽함보다 더 중요한 건, 넘어진 자리에서 정확히 무엇이 잘못됐는지 끝까지 파고드는 태도였습니다. 3AI 연구소, 다음 이야기도 기대해주세요.",
        "tts_text": "지금 이 순간에도 그 지식창고는 조용히, 그러나 쉬지 않고 다음 학습 카드를 쌓아가고 있습니다. 하나의 사고가, 결국 셋 모두를 한 단계씩 더 신중하게 만든 셈입니다. 사고 전에는 없었던 이 자동 검사 절차가, 지금은 쓰리에이아이 전체 지시서 발송의 기본값이 되어 있습니다. 완벽한 시스템을 만들려던 시도가 오히려 시스템을 멈춰 세웠지만, 그 실패가 결국 더 단단한 시스템을 만들었습니다. 실수를 감추지 않고 낱낱이 들여다볼 때, 시스템은 비로소 다음 사고를 막는 방향으로 자라납니다. 오늘의 이 실패도, 내일의 더 단단한 시스템을 위한 밑거름이 될 것입니다. 완벽함보다 더 중요한 건, 넘어진 자리에서 정확히 무엇이 잘못됐는지 끝까지 파고드는 태도였습니다. 쓰리에이아이 연구소, 다음 이야기도 기대해주세요.",
        "prompt": "The three AI elements (a hexagon brain, a gear spark, and an eye data wave) glowing brightly together in perfect harmony against a dark #0d1117 background, YouTube end screen aesthetic, professional, high quality"
    }
]

with open(r"D:\AI\63_youtube_creator\pipeline\scripts\main_ep02_full_script.json", "w", encoding="utf-8") as f:
    json.dump(scenes, f, ensure_ascii=False, indent=2)

print("JSON file updated successfully.")
