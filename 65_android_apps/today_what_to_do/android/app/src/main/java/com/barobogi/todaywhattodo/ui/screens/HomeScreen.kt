package com.barobogi.todaywhattodo.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.barobogi.todaywhattodo.ui.theme.PrimaryBlue

@Composable
fun HomeScreen(
    onNavigateToCondition: (String) -> Unit,
    onNavigateToSaved: () -> Unit,
    onNavigateToMyPage: () -> Unit
) {
    Scaffold(
        topBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "오늘뭐하지 🎈",
                        fontSize = 22.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onBackground
                    )
                    Text(
                        text = "📍 서울 중구 (현재 26°C · 맑음)",
                        fontSize = 13.sp,
                        color = Color.Gray
                    )
                }
                Row {
                    IconButton(onClick = onNavigateToSaved) {
                        Text("⭐", fontSize = 20.sp)
                    }
                    IconButton(onClick = onNavigateToMyPage) {
                        Text("👤", fontSize = 20.sp)
                    }
                }
            }
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // 1. 핵심 바로가기 메인 배너
            item {
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { onNavigateToCondition("7세 아이") },
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = PrimaryBlue)
                ) {
                    Column(modifier = Modifier.padding(20.dp)) {
                        Text(
                            text = "지금 어디 갈지 고민된다면?",
                            color = Color.White.copy(alpha = 0.8f),
                            fontSize = 14.sp
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(
                            text = "3초 만에 오늘 맞춤 코스 찾기 ➔",
                            color = Color.White,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }

            // 2. 상황별 추천 칩 목록
            item {
                Text(
                    text = "누구와 함께 가시나요?",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.SemiBold
                )
                Spacer(modifier = Modifier.height(10.dp))
                val companions = listOf(
                    "👶 7세 아이와" to "7세 아이",
                    "🐾 댕댕이와 함께" to "반려동물",
                    "💑 연인과 데이트" to "연인",
                    "🏃 나 혼자 힐링" to "혼자",
                    "👵 부모님과 산책" to "부모님"
                )
                LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(companions) { (label, value) ->
                        SuggestionChip(
                            onClick = { onNavigateToCondition(value) },
                            label = { Text(label, fontSize = 14.sp) }
                        )
                    }
                }
            }

            // 3. 실시간 인기 테마
            item {
                Text(
                    text = "오늘의 인기 테마 🔥",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.SemiBold
                )
                Spacer(modifier = Modifier.height(10.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("🏛️ 비 오는 날 가기 좋은 실내 박물관 TOP 5", fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(4.dp))
                        Text("국립어린이과학관, 서울애니메이션센터 만화의집 등", fontSize = 13.sp, color = Color.Gray)
                    }
                }
            }
        }
    }
}
