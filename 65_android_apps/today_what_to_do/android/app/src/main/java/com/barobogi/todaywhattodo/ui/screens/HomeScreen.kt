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

data class ThemeCardItem(
    val title: String,
    val subtitle: String,
    val tags: List<String>,
    val companionFilter: String,
    val preferIndoor: Boolean = false
)

@Composable
fun HomeScreen(
    viewModel: RecommendViewModel,
    onNavigateToCondition: (String) -> Unit,
    onNavigateToSaved: () -> Unit,
    onNavigateToMyPage: () -> Unit
) {
    val locationText = if (viewModel.locationName.isNotBlank() && !viewModel.locationName.contains("탐색")) {
        "📍 ${viewModel.locationName} (현재 26°C · 맑음)"
    } else {
        "📍 GPS 실시간 위치 탐색 중... (현재 26°C)"
    }

    val themeList = listOf(
        ThemeCardItem(
            title = "🏛️ 비 오는 날 필수! 실내 박물관 & 미술관 TOP 5",
            subtitle = "수원시립미술관 · 국립지도박물관 · 국립어린이과학관",
            tags = listOf("#실내추천", "#키즈존", "#공공데이터검증"),
            companionFilter = "7세 아이",
            preferIndoor = true
        ),
        ThemeCardItem(
            title = "🌳 아이와 가기 좋은 도심 숲속 공원 TOP 5",
            subtitle = "광교호수공원 · 경기상상캠퍼스 · 율동공원 산책로",
            tags = listOf("#유모차산책", "#무료입장", "#피크닉"),
            companionFilter = "7세 아이",
            preferIndoor = false
        ),
        ThemeCardItem(
            title = "☕ 분위기 좋은 대형 베이커리 카페 & 뷰 맛집 TOP 5",
            subtitle = "행궁동 성곽길 카페 · 광교 수변 카페 · 보정동 카페거리",
            tags = listOf("#데이트", "#뷰맛집", "#주차가능"),
            companionFilter = "연인",
            preferIndoor = true
        ),
        ThemeCardItem(
            title = "🐾 댕댕이와 함께 달리는 펫 안심 테마파크 TOP 5",
            subtitle = "광교 펫 파크 · 경기상상캠퍼스 펫존 · 율동공원 펫파크",
            tags = listOf("#반려동물동반", "#잔디밭", "#안심공간"),
            companionFilter = "반려동물",
            preferIndoor = false
        ),
        ThemeCardItem(
            title = "🌃 야간 경관 조명 야경 데이트 명소 TOP 5",
            subtitle = "수원화성 야간개장 · 남산 서울타워 · 광교호수 야경",
            tags = listOf("#야경명소", "#야간데이트", "#인생샷"),
            companionFilter = "연인",
            preferIndoor = false
        )
    )

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

            // 3. 실시간 인기 테마 5종 카드 리스트 (5개 테마 전수 노출)
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "오늘의 실시간 인기 테마 TOP 5 🔥",
                        fontSize = 17.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Text("전체 5개", fontSize = 12.sp, color = PrimaryBlue, fontWeight = FontWeight.Bold)
                }
            }

            items(themeList) { theme ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable {
                            viewModel.currentCompanion = theme.companionFilter
                            viewModel.preferIndoor = theme.preferIndoor
                            onNavigateToCondition(theme.companionFilter)
                        },
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                            Text(theme.title, fontWeight = FontWeight.Bold, fontSize = 15.sp, modifier = Modifier.weight(1f))
                            Text("🔥 핫플", fontSize = 12.sp, color = PrimaryBlue, fontWeight = FontWeight.Bold)
                        }
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(theme.subtitle, fontSize = 13.sp, color = Color.Gray)
                        Spacer(modifier = Modifier.height(10.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            theme.tags.forEach { tag ->
                                Surface(
                                    shape = RoundedCornerShape(6.dp),
                                    color = PrimaryBlue.copy(alpha = 0.1f)
                                ) {
                                    Text(
                                        text = tag,
                                        fontSize = 11.sp,
                                        color = PrimaryBlue,
                                        fontWeight = FontWeight.Medium,
                                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 3.dp)
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
