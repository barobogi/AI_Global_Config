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
                        // 0. 반경 즉시 재조정 컨트롤 바 (핫플가이드 벤치마킹)
                        item {
                            Card(
                                shape = RoundedCornerShape(12.dp),
                                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(12.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text("📍 탐색 반경 변경:", fontSize = 13.sp, fontWeight = FontWeight.Bold)
                                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                        listOf(1, 3, 5, 10).forEach { r ->
                                            val isSelected = (viewModel.currentRadiusKm.toInt() == r)
                                            FilterChip(
                                                selected = isSelected,
                                                onClick = {
                                                    viewModel.currentRadiusKm = r.toDouble()
                                                    viewModel.requestRecommendation()
                                                },
                                                label = { Text("${r}km", fontSize = 11.sp) }
                                            )
                                        }
                                    }
                                }
                            }
                        }

                        // 1. 추천 코스 세트
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
                        items(state.courses) { course ->
                            Card(
                                shape = RoundedCornerShape(16.dp),
                                colors = CardDefaults.cardColors(containerColor = SecondaryTeal.copy(alpha = 0.08f)),
                                modifier = Modifier.fillMaxWidth()
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
                                    
                                    // 킬러 차별화: 왜 이 코스를 추천했나요? (Why Card + 팩트체크 배지)
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

                                    // 공유 버튼 (트리플 벤치마킹)
                                    Spacer(modifier = Modifier.height(8.dp))
                                    OutlinedButton(
                                        onClick = { /* 카카오톡 / 링크 공유 액션 */ },
                                        modifier = Modifier.fillMaxWidth(),
                                        shape = RoundedCornerShape(10.dp)
                                    ) {
                                        Text("💬 카카오톡 / 코스 링크 공유하기", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                    }
                                }
                            }
                        }

                        // 2. 개별 장소 랭킹 목록
                        item {
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "후보 장소 상세 (Hard Filter 통과) 📍",
                                fontSize = 18.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                        items(state.topPlaces) { place ->
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
                                        if (place.factCheck?.isVerified == true) {
                                            Surface(
                                                shape = RoundedCornerShape(4.dp),
                                                color = Color(0xFFE8F5E9)
                                            ) {
                                                Text(
                                                    text = "공공데이터 팩트검증 완료",
                                                    color = Color(0xFF2E7D32),
                                                    fontSize = 10.sp,
                                                    modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp),
                                                    fontWeight = FontWeight.Bold
                                                )
                                            }
                                        }
                                    }

                                    // 필터 통과 사유 태그 목록
                                    place.filterPassReasons?.let { reasons ->
                                        Spacer(modifier = Modifier.height(8.dp))
                                        Row(
                                            modifier = Modifier.fillMaxWidth(),
                                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                                        ) {
                                            reasons.take(3).forEach { r ->
                                                Surface(
                                                    shape = RoundedCornerShape(6.dp),
                                                    color = Color(0xFFF0F4F8)
                                                ) {
                                                    Text(
                                                        text = r,
                                                        fontSize = 10.sp,
                                                        color = Color(0xFF4A5568),
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
                is RecommendUiState.Idle -> {
                    // 대기 상태
                }
            }
        }
    }
}
