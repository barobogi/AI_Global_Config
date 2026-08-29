package com.barobogi.todaywhattodo.ui.screens

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
import com.barobogi.todaywhattodo.viewmodel.RecommendViewModel

@Composable
fun HomeScreen(
    viewModel: RecommendViewModel,
    onNavigateToCondition: (String) -> Unit,
    onNavigateToSaved: () -> Unit,
    onNavigateToMyPage: () -> Unit
) {
    val locationText = if (viewModel.locationName.isNotBlank() && viewModel.locationName != "위치 탐색 중...") {
        "📍 ${viewModel.locationName} (현재 26°C · 맑음)"
    } else {
        "📍 GPS 실시간 위치 탐색 중... (현재 26°C)"
    }

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
                        text = locationText,
                        fontSize = 13.sp,
                        color = MaterialTheme.colorScheme.primary
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
            verticalArrangement = Arrangement.spacedBy(18.dp)
        ) {
            // 1. 핵심 바로가기 메인 배너 (그래디언트 톤)
            item {
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { onNavigateToCondition(viewModel.currentCompanion) },
                    shape = RoundedCornerShape(20.dp),
                    colors = CardDefaults.cardColors(containerColor = PrimaryBlue)
                ) {
                    Column(modifier = Modifier.padding(22.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = Color.White.copy(alpha = 0.2f)
                            ) {
                                Text(
                                    text = "AI 3중 팩트체크 교차검증 🛡️",
                                    color = Color.White,
                                    fontSize = 11.sp,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                        Spacer(modifier = Modifier.height(10.dp))
                        Text(
                            text = "오늘 어디 갈지 고민된다면?",
                            color = Color.White.copy(alpha = 0.9f),
                            fontSize = 14.sp
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "3초 만에 내 주변 맞춤 코스 찾기 ➔",
                            color = Color.White,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }

            // 2. 동행자 맞춤 선택 (세분화 칩)
            item {
                Text(
                    text = "누구와 함께 가시나요? 👥",
                    fontSize = 17.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(10.dp))
                val companions = listOf(
                    "👶 영유아(0~3세)" to "영유아",
                    "🧒 어린이(4~7세)" to "7세 아이",
                    "🎒 초등학생" to "초등학생",
                    "💑 연인과 데이트" to "연인",
                    "🐾 댕댕이와 함께" to "반려동물",
                    "👵 부모님과 산책" to "부모님",
                    "👥 친구들과 모임" to "친구",
                    "🏃 나 혼자 힐링" to "혼자"
                )
                LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(companions) { pair ->
                        val label = pair.first
                        val value = pair.second
                        SuggestionChip(
                            onClick = {
                                viewModel.currentCompanion = value
                                onNavigateToCondition(value)
                            },
                            label = { Text(label, fontSize = 13.sp, fontWeight = FontWeight.Medium) }
                        )
                    }
                }
            }

            // 3. 실시간 인기 테마 롤링 배너 Cards
            item {
                Text(
                    text = "오늘의 실시간 인기 테마 🔥",
                    fontSize = 17.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(10.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                            Text("🏛️ 비 오는 날 필수! 실내 박물관 TOP 5", fontWeight = FontWeight.Bold, fontSize = 15.sp)
                            Text("🔥 핫플", fontSize = 12.sp, color = PrimaryBlue, fontWeight = FontWeight.Bold)
                        }
                        Spacer(modifier = Modifier.height(6.dp))
                        Text("국립어린이과학관 · 서울애니메이션센터 · 국립현대미술관", fontSize = 13.sp, color = Color.Gray)
                        Spacer(modifier = Modifier.height(10.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            SuggestionChip(onClick = {}, label = { Text("#주차가능", fontSize = 11.sp) })
                            SuggestionChip(onClick = {}, label = { Text("#키즈존", fontSize = 11.sp) })
                            SuggestionChip(onClick = {}, label = { Text("#공공데이터검증", fontSize = 11.sp) })
                        }
                    }
                }
            }
        }
    }
}
