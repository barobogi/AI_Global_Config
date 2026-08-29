package com.barobogi.todaywhattodo.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
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
            Surface(
                shadowElevation = 4.dp,
                color = MaterialTheme.colorScheme.surface
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 8.dp, vertical = 12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    IconButton(onClick = onBack) {
                        Text("◀", fontSize = 18.sp, color = MaterialTheme.colorScheme.onSurface)
                    }
                    Text(
                        text = "오늘의 3AI 맞춤 추천 ✨",
                        fontSize = 19.sp,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Spacer(modifier = Modifier.width(40.dp))
                }
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
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier.padding(24.dp)
                    ) {
                        CircularProgressIndicator(color = PrimaryBlue, strokeWidth = 4.dp)
                        Spacer(modifier = Modifier.height(20.dp))
                        Text(
                            text = "3AI 팩트체크 교차 검증 중... 🛡️",
                            fontWeight = FontWeight.Bold,
                            fontSize = 17.sp,
                            color = PrimaryBlue
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(
                            text = "💡 첫 요청 시 3AI 백엔드 서버 기동으로 최대 1분 소요될 수 있습니다",
                            fontSize = 12.sp,
                            color = Color.Gray
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "한국관광공사 국문 공공데이터 원본 3중 팩트체크 중",
                            fontSize = 11.sp,
                            color = Color.LightGray
                        )
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
                    verticalArrangement = Arrangement.spacedBy(18.dp),
                    contentPadding = PaddingValues(vertical = 16.dp)
                ) {
                    // 0. 반경 즉시 변경 칩 (1km, 3km, 5km, 10km, 20km)
                    item {
                        Surface(
                            shape = RoundedCornerShape(14.dp),
                            color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(horizontal = 14.dp, vertical = 10.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("📍 반경 변경:", fontSize = 13.sp, fontWeight = FontWeight.Bold)
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
                                            label = { Text("${r.toInt()}km", fontSize = 12.sp, fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal) }
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
                                Surface(
                                    shape = RoundedCornerShape(6.dp),
                                    color = PrimaryBlue.copy(alpha = 0.12f)
                                ) {
                                    Text(
                                        text = "💡 ${viewModel.currentCompanion} 맞춤",
                                        fontSize = 11.sp,
                                        color = PrimaryBlue,
                                        fontWeight = FontWeight.Bold,
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                    )
                                }
                            }
                        }
                        items(courses) { course ->
                            Card(
                                shape = RoundedCornerShape(20.dp),
                                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .border(1.dp, PrimaryBlue.copy(alpha = 0.2f), RoundedCornerShape(20.dp))
                                    .clickable {
                                        if (topPlaces.isNotEmpty()) {
                                            onPlaceClick(topPlaces.first())
                                        }
                                    }
                            ) {
                                Column(modifier = Modifier.padding(18.dp)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            text = course.courseName,
                                            fontWeight = FontWeight.Bold,
                                            fontSize = 17.sp,
                                            color = PrimaryBlue
                                        )
                                        Surface(
                                            shape = RoundedCornerShape(8.dp),
                                            color = SecondaryTeal.copy(alpha = 0.15f)
                                        ) {
                                            Text(
                                                text = "⏱️ 약 ${course.durationHours}시간",
                                                fontSize = 11.sp,
                                                color = SecondaryTeal,
                                                fontWeight = FontWeight.Bold,
                                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                            )
                                        }
                                    }

                                    Spacer(modifier = Modifier.height(8.dp))
                                    Text(
                                        text = course.aiReason ?: course.summary,
                                        fontSize = 13.sp,
                                        lineHeight = 19.sp,
                                        color = MaterialTheme.colorScheme.onSurface
                                    )

                                    // Why Card + 팩트체크 배지
                                    Spacer(modifier = Modifier.height(12.dp))
                                    Surface(
                                        shape = RoundedCornerShape(12.dp),
                                        color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f),
                                        modifier = Modifier.fillMaxWidth()
                                    ) {
                                        Column(modifier = Modifier.padding(12.dp)) {
                                            Row(
                                                modifier = Modifier.fillMaxWidth(),
                                                horizontalArrangement = Arrangement.SpaceBetween,
                                                verticalAlignment = Alignment.CenterVertically
                                            ) {
                                                Text(
                                                    text = "🔍 3AI 추천 근거",
                                                    fontSize = 12.sp,
                                                    fontWeight = FontWeight.Bold,
                                                    color = PrimaryBlue
                                                )
                                                Surface(
                                                    shape = RoundedCornerShape(4.dp),
                                                    color = Color(0xFFE8F5E9)
                                                ) {
                                                    Text(
                                                        text = "공공데이터 3중 팩트체크 🛡️",
                                                        fontSize = 10.sp,
                                                        color = Color(0xFF2E7D32),
                                                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
                                                        fontWeight = FontWeight.Bold
                                                    )
                                                }
                                            }
                                            Spacer(modifier = Modifier.height(6.dp))
                                            course.whyCard?.badges?.forEach { badge ->
                                                Text(text = "• $badge", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f))
                                            }
                                        }
                                    }

                                    Spacer(modifier = Modifier.height(10.dp))
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.End,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            text = "코용 상세 및 리뷰 보기 ➔",
                                            fontSize = 12.sp,
                                            color = PrimaryBlue,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }
                                }
                            }
                        }
                    }

                    // 2. 개별 장소 랭킹 목록 (이미지 썸네일 + 타이트 깔끔 카드 레이아웃)
                    item {
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "추천 장소 상세 리스트 📍",
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "장소를 누르면 상세 소개, 위치 길찾기 및 1,000+개 실시간 이용후기를 확인합니다.",
                            fontSize = 12.sp,
                            color = Color.Gray
                        )
                    }

                    items(topPlaces) { place ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { onPlaceClick(place) },
                            shape = RoundedCornerShape(18.dp),
                            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                        ) {
                            Column {
                                // 1. 상단 히어로 썸네일 이미지 (또는 풍성한 그래디언트 바)
                                val imgUrl = place.firstImage
                                if (!imgUrl.isNull_or_blank_check(imgUrl)) {
                                    AsyncImage(
                                        model = imgUrl,
                                        contentDescription = place.title,
                                        contentScale = ContentScale.Crop,
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .height(130.dp)
                                            .clip(RoundedCornerShape(topStart = 18.dp, topEnd = 18.dp))
                                    )
                                } else {
                                    // 고화질 테마 그래디언트 믹스
                                    Box(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .height(80.dp)
                                            .background(
                                                Brush.horizontalGradient(
                                                    colors = listOf(PrimaryBlue, SecondaryTeal)
                                                )
                                            )
                                            .padding(14.dp),
                                        contentAlignment = Alignment.CenterStart
                                    ) {
                                        Row(
                                            modifier = Modifier.fillMaxWidth(),
                                            horizontalArrangement = Arrangement.SpaceBetween,
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Text(
                                                text = getCategoryEmoji(place.title),
                                                fontSize = 28.sp
                                            )
                                            Surface(
                                                shape = RoundedCornerShape(8.dp),
                                                color = Color.White.copy(alpha = 0.25f)
                                            ) {
                                                Text(
                                                    text = "공공데이터 팩트체크 🛡️",
                                                    fontSize = 11.sp,
                                                    color = Color.White,
                                                    fontWeight = FontWeight.Bold,
                                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                                )
                                            }
                                        }
                                    }
                                }

                                // 2. 타이트 본문 영역 (빈 공간 없이 꽉 차고 정돈된 패킹)
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.Top
                                    ) {
                                        Column(modifier = Modifier.weight(1f)) {
                                            Text(
                                                text = place.title,
                                                fontWeight = FontWeight.Bold,
                                                fontSize = 17.sp,
                                                maxLines = 1,
                                                overflow = TextOverflow.Ellipsis
                                            )
                                            Spacer(modifier = Modifier.height(4.dp))
                                            Text(
                                                text = place.address ?: "주소 정보 등록 중",
                                                fontSize = 13.sp,
                                                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
                                                maxLines = 1,
                                                overflow = TextOverflow.Ellipsis
                                            )
                                        }
                                        Spacer(modifier = Modifier.width(8.dp))
                                        Surface(
                                            shape = RoundedCornerShape(10.dp),
                                            color = PrimaryBlue
                                        ) {
                                            Text(
                                                text = "${place.finalScore?.toInt() ?: 90}점",
                                                color = Color.White,
                                                fontWeight = FontWeight.Bold,
                                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp),
                                                fontSize = 13.sp
                                            )
                                        }
                                    }

                                    Spacer(modifier = Modifier.height(10.dp))

                                    // 정보 칩 태그
                                    val fee = place.detailIntro?.useFeeCulture ?: place.detailIntro?.useFee ?: "무료/기본입장"
                                    Row(
                                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                                        verticalAlignment = Alignment.CenterVertically,
                                        modifier = Modifier.fillMaxWidth()
                                    ) {
                                        Surface(
                                            shape = RoundedCornerShape(6.dp),
                                            color = PrimaryBlue.copy(alpha = 0.1f)
                                        ) {
                                            Text(
                                                text = "💰 ${fee.take(18)}",
                                                fontSize = 11.sp,
                                                color = PrimaryBlue,
                                                fontWeight = FontWeight.Bold,
                                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 3.dp),
                                                maxLines = 1
                                            )
                                        }
                                        Surface(
                                            shape = RoundedCornerShape(6.dp),
                                            color = Color.Gray.copy(alpha = 0.12f)
                                        ) {
                                            Text(
                                                text = "📍 약 ${place.distanceKm ?: 0.0}km",
                                                fontSize = 11.sp,
                                                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.8f),
                                                fontWeight = FontWeight.Medium,
                                                modifier = Modifier.padding(horizontal = 6.dp, vertical = 3.dp)
                                            )
                                        }
                                    }

                                    Spacer(modifier = Modifier.height(12.dp))
                                    Divider(color = Color.Gray.copy(alpha = 0.15f))
                                    Spacer(modifier = Modifier.height(10.dp))

                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(
                                            text = "💬 실제 방문자 리뷰 & 상세 소개",
                                            fontSize = 12.sp,
                                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                                        )
                                        Text(
                                            text = "상세보기 ➔",
                                            fontSize = 12.sp,
                                            color = PrimaryBlue,
                                            fontWeight = FontWeight.Bold
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
}

private fun String?.isNull_or_blank_check(str: String?): Boolean {
    return str == null || str.isBlank() || str.contains("null")
}

private fun getCategoryEmoji(title: String): String {
    return when {
        title.contains("박물관") || title.contains("미술관") -> "🏛️"
        title.contains("공원") || title.contains("숲") || title.contains("호수") -> "🌳"
        title.contains("카페") || title.contains("베이커리") -> "☕"
        title.contains("식당") || title.contains("갈비") || title.contains("맛집") -> "🍴"
        else -> "🎈"
    }
}
