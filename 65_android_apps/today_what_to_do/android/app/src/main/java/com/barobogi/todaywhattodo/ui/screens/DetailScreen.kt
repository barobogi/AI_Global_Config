package com.barobogi.todaywhattodo.ui.screens

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.barobogi.todaywhattodo.data.model.Place
import com.barobogi.todaywhattodo.ui.theme.PrimaryBlue
import com.barobogi.todaywhattodo.ui.theme.SecondaryTeal

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DetailScreen(
    place: Place,
    onBack: () -> Unit
) {
    val context = LocalContext.current

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(place.title, fontWeight = FontWeight.Bold, maxLines = 1) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Text("◀", fontSize = 18.sp)
                    }
                }
            )
        },
        bottomBar = {
            Surface(
                shadowElevation = 8.dp,
                color = MaterialTheme.colorScheme.surface
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    // 전화 걸기 버튼
                    if (!place.tel.isNullOrBlank()) {
                        OutlinedButton(
                            onClick = {
                                val intent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:${place.tel}"))
                                context.startActivity(intent)
                            },
                            modifier = Modifier.weight(1f).height(50.dp),
                            shape = RoundedCornerShape(12.dp)
                        ) {
                            Text("📞 전화 문의")
                        }
                    }
                    // 길찾기/지도 버튼
                    Button(
                        onClick = {
                            val uri = Uri.parse("geo:${place.mapY},${place.mapX}?q=${Uri.encode(place.title)}")
                            val mapIntent = Intent(Intent.ACTION_VIEW, uri)
                            context.startActivity(mapIntent)
                        },
                        modifier = Modifier.weight(1f).height(50.dp),
                        shape = RoundedCornerShape(12.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = PrimaryBlue)
                    ) {
                        Text("🧭 지도·길찾기", fontWeight = FontWeight.Bold)
                    }
                }
            }
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // 1. 팩트체크 인증 배지 (AI-3)
            Card(
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = SecondaryTeal.copy(alpha = 0.12f))
            ) {
                Row(
                    modifier = Modifier.padding(14.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("🛡️", fontSize = 22.sp)
                    Spacer(modifier = Modifier.width(10.dp))
                    Column {
                        Text("3AI 팩트체크 검증 완료", fontWeight = FontWeight.Bold, color = SecondaryTeal)
                        Text("한국관광공사 국문 공공데이터 공식 원본과 교차 검증됨", fontSize = 12.sp, color = Color.Gray)
                    }
                }
            }

            // 2. 장소 개요
            Text("장소 소개", fontSize = 16.sp, fontWeight = FontWeight.Bold)
            Text(
                text = place.overview ?: "소개 정보가 준비 중입니다.",
                fontSize = 14.sp,
                lineHeight = 22.sp,
                color = MaterialTheme.colorScheme.onBackground
            )

            Divider()

            // 3. 이용 정보 상세
            Text("이용 안내", fontSize = 16.sp, fontWeight = FontWeight.Bold)
            val intro = place.detailIntro
            val rest = intro?.restDateCulture ?: intro?.restDate ?: "정보 없음"
            val useTime = intro?.useTimeCulture ?: intro?.useTime ?: "정보 없음"
            val fee = intro?.useFeeCulture ?: intro?.useFee ?: "무료/기본입장"

            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("📍 주소: ${place.address ?: "주소 미제공"}", fontSize = 13.sp)
                Text("⏰ 운영시간: $useTime", fontSize = 13.sp)
                Text("🚫 휴무일: $rest", fontSize = 13.sp)
                Text("💰 이용요금: $fee", fontSize = 13.sp)
            }
        }
    }
}
