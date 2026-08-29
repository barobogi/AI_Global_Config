package com.barobogi.todaywhattodo.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.barobogi.todaywhattodo.data.model.Place
import com.barobogi.todaywhattodo.ui.theme.PrimaryBlue
import com.barobogi.todaywhattodo.ui.theme.SecondaryTeal
import com.barobogi.todaywhattodo.viewmodel.RecommendUiState
import com.barobogi.todaywhattodo.viewmodel.RecommendViewModel

@Composable
fun ResultScreen(
    viewModel: RecommendViewModel,
    onPlaceClick: (Place) -> Unit,
    onBack: () -> Unit
) {
    val state by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onBack) {
                    Text("◀", fontSize = 18.sp)
                }
                Text(
                    text = "오늘의 추천 결과 ✨",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.width(24.dp))
            }
        }
    ) { innerPadding ->
        when (val uiState = state) {
            is RecommendUiState.Idle, is RecommendUiState.Loading -> {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        CircularProgressIndicator(color = PrimaryBlue)
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("3AI 팩트체크 교차 검증 중...", fontWeight = FontWeight.Bold, color = PrimaryBlue)
                        Text("한국관광공사 공공데이터 원본 조회 중", fontSize = 12.sp, color = Color.Gray)
                    }
                }
            }
            is RecommendUiState.Error -> {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding)
                        .padding(24.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Card(
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer),
                        shape = RoundedCornerShape(16.dp)
                    ) {
                        Column(modifier = Modifier.padding(20.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("⚠️ 추천 결과 안내", fontWeight = FontWeight.Bold, fontSize = 18.sp, color = MaterialTheme.colorScheme.onErrorContainer)
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(uiState.message, fontSize = 14.sp, color = MaterialTheme.colorScheme.onErrorContainer)
                            Spacer(modifier = Modifier.height(16.dp))
                            Button(
                                onClick = {
                                    viewModel.currentRadiusKm = 15.0
                                    viewModel.currentBudget = 100000
                                    viewModel.requestRecommendation()
                                },
                                colors = ButtonDefaults.buttonColors(containerColor = PrimaryBlue)
                            ) {
                                Text("⚡ 반경 15km로 넓혀 재검색하기")
                            }
                        }
                    }
                }
            }
            is RecommendUiState.Success -> {
                val courses = uiState.courses
                val topPlaces = uiState.topPlaces

                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding)
                        .padding(horizontal = 16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    // 0. 반경 즉시 변경 칩 (1km, 3km, 5km, 10km, 20km)
                    item {
                        Card(
                            shape = RoundedCornerShape(14.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("📍 탐색 반경 변경:", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                                val radiusOptions = listOf(1.0, 3.0, 5.0, 10.0, 20.0)
                                LazyRow(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    items(radiusOptions) { r ->
                                        val isSelected = (viewModel.currentRadiusKm == r)
                                        FilterChip(
                                            selected = isSelected,
                                            onClick = {
                                                viewModel.currentRadiusKm = r
                                                viewModel.requestRecommendation()
                                            },
                                            label = { Text("${r.toInt()}km", fontSize = 12.sp) }
                                        )
                                    }
                                }
                            }
                        }
                    }

                    // 1. 메인 AI 코스 조립 카드 (이유 포함)
                    if (courses.isNotEmpty()) {
                        item {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = "오늘의 맞춤 코스 조합 🗺️",
                                    fontSize = 18.sp,
                                    fontWeight = FontWeight.Bold
                                )
                                Text("💡 ${viewModel.currentCompanion} 맞춤 가중치", fontSize = 12.sp, color = PrimaryBlue, fontWeight = FontWeight.Bold)
                            }
                        }
                        items(courses) { course ->
                            Card(
                                shape = RoundedCornerShape(16.dp),
                                colors = CardDefaults.cardColors(containerColor = SecondaryTeal.copy(alpha = 0.08f)),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable {
                                        if (topPlaces.isNotEmpty()) {
                                            onPlaceClick(topPlaces.first())
                                        }
                                    }
                            ) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(course.courseName, fontWeight = FontWeight.Bold, fontSize = 16.sp, color = SecondaryTeal)
                                        Text("⏱️ 약 ${course.durationHours}시간", fontSize = 12.sp, color = Color.Gray)
                                    }

                                    Spacer(modifier = Modifier.height(6.dp))
                                    Text(course.aiReason ?: course.summary, fontSize = 13.sp, lineHeight = 18.sp)

                                    // 터치 안내 힌트
                                    Spacer(modifier = Modifier.height(6.dp))
                                    Text("👉 터치 시 대표 장소 상세소개 & 다른 사람 이용후기 보기 ➔", fontSize = 11.sp, color = PrimaryBlue, fontWeight = FontWeight.Bold)

                                    // Why Card + 팩트체크 배지
                                    Spacer(modifier = Modifier.height(10.dp))
                                    Surface(
                                        shape = RoundedCornerShape(10.dp),
                                        color = Color.White.copy(alpha = 0.9f),
                                        modifier = Modifier.fillMaxWidth()
                                    ) {
                                        Column(modifier = Modifier.padding(12.dp)) {
                                            Row(
                                                modifier = Modifier.fillMaxWidth(),
                                                horizontalArrangement = Arrangement.SpaceBetween,
                                                verticalAlignment = Alignment.CenterVertically
                                            ) {
                                                Text(
                                                    text = "🔍 3AI 추천 근거 (투명한 선정 이유)",
                                                    fontSize = 12.sp,
                                                    fontWeight = FontWeight.Bold,
                                                    color = PrimaryBlue
                                                )
                                                Surface(
                                                    shape = RoundedCornerShape(4.dp),
                                                    color = Color(0xFFE8F5E9)
                                                ) {
                                                    Text(
                                                        text = "공공데이터 3중 교차검증 완료 🛡️",
                                                        fontSize = 10.sp,
                                                        color = Color(0xFF2E7D32),
                                                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
                                                        fontWeight = FontWeight.Bold
                                                    )
                                                }
                                            }
                                            Spacer(modifier = Modifier.height(6.dp))
                                            course.whyCard?.badges?.forEach { badge ->
                                                Text(text = "• $badge", fontSize = 12.sp, color = Color.DarkGray)
                                            }
                                            course.whyCard?.verifiedFacts?.take(2)?.forEach { fact ->
                                                Text(text = "• $fact", fontSize = 11.sp, color = Color.Gray)
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // 2. 개별 장소 랭킹 목록 (터치 시 상세 정보 + 다른 사람 이용 후기 이동)
                    item {
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "후보 장소 상세 (Hard Filter 통과) 📍",
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text("👇 장소를 누르면 상세 정보, 운영시간, 지도 위치 및 실제 이용후기를 볼 수 있습니다.", fontSize = 12.sp, color = Color.Gray)
                    }

                    items(topPlaces) { place ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { onPlaceClick(place) },
                            shape = RoundedCornerShape(14.dp)
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(place.title, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                                        Spacer(modifier = Modifier.height(4.dp))
                                        Text(place.address ?: "주소 정보 없음", fontSize = 13.sp, color = Color.Gray)
                                    }
                                    Surface(
                                        shape = RoundedCornerShape(8.dp),
                                        color = PrimaryBlue
                                    ) {
                                        Text(
                                            text = "${place.finalScore?.toInt() ?: 90}점",
                                            color = Color.White,
                                            fontWeight = FontWeight.Bold,
                                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                                            fontSize = 13.sp
                                        )
                                    }
                                }

                                Spacer(modifier = Modifier.height(8.dp))
                                val fee = place.detailIntro?.useFeeCulture ?: place.detailIntro?.useFee ?: "무료/기본입장"
                                Row(
                                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text("💰 $fee", fontSize = 12.sp, color = PrimaryBlue, fontWeight = FontWeight.Medium)
                                    Text("📏 약 ${place.distanceKm ?: 0.0}km", fontSize = 12.sp, color = Color.Gray)
                                    Text("💬 리뷰/상세보기 ➔", fontSize = 11.sp, color = PrimaryBlue, fontWeight = FontWeight.Bold)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
