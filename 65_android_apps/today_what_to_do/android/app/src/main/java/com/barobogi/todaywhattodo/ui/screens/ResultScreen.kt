package com.barobogi.todaywhattodo.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
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

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResultScreen(
    viewModel: RecommendViewModel,
    onPlaceClick: (Place) -> Unit,
    onBack: () -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("오늘의 추천 결과 ✨", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Text("◀", fontSize = 18.sp)
                    }
                }
            )
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            when (val state = uiState) {
                is RecommendUiState.Loading -> {
                    Column(
                        modifier = Modifier.fillMaxSize(),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        CircularProgressIndicator(color = PrimaryBlue)
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("공공데이터와 날씨를 분석하여 최적 코스를 찾는 중...", color = Color.Gray)
                    }
                }
                is RecommendUiState.Error -> {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(24.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Text("⚠️", fontSize = 40.sp)
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(state.message, color = Color.Red, fontWeight = FontWeight.Medium)
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(onClick = { viewModel.requestRecommendation() }) {
                            Text("다시 시도")
                        }
                    }
                }
                is RecommendUiState.Success -> {
                    LazyColumn(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(horizontal = 16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        // 1. 추천 코스 세트
                        item {
                            Text(
                                text = "추천 코스 조합 🗺️",
                                fontSize = 17.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                        items(state.courses) { course ->
                            Card(
                                shape = RoundedCornerShape(12.dp),
                                colors = CardDefaults.cardColors(containerColor = SecondaryTeal.copy(alpha = 0.1f))
                            ) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Text(course.courseName, fontWeight = FontWeight.Bold, color = SecondaryTeal)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(course.summary, fontSize = 13.sp)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text("⏱️ 예상 소요: 약 ${course.durationHours}시간", fontSize = 12.sp, color = Color.Gray)
                                }
                            }
                        }

                        // 2. 개별 장소 랭킹 목록
                        item {
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "개별 추천 장소 목록 (Hard Filter 통과) 📍",
                                fontSize = 17.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                        items(state.topPlaces) { place ->
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { onPlaceClick(place) },
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(16.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(place.title, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                                        Spacer(modifier = Modifier.height(4.dp))
                                        Text(place.address ?: "주소 정보 없음", fontSize = 13.sp, color = Color.Gray)
                                        Spacer(modifier = Modifier.height(4.dp))
                                        val fee = place.detailIntro?.useFeeCulture ?: place.detailIntro?.useFee ?: "무료/기본입장"
                                        Text("💰 $fee · 📏 약 ${place.distanceKm ?: 0.0}km", fontSize = 12.sp, color = PrimaryBlue)
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
                                            fontSize = 14.sp
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
                is RecommendUiState.Idle -> {
                    // 대기 상태
                }
            }
        }
    }
}
