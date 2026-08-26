package com.barobogi.todaywhattodo.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MyPageScreen(onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("설정 및 정보 👤", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Text("◀", fontSize = 18.sp)
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Card(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("오늘뭐하지 (Today What To Do)", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Text("버전 1.0.0 (MVP)", fontSize = 13.sp, color = Color.Gray)
                }
            }

            Text("데이터 제공 출처", fontWeight = FontWeight.SemiBold, fontSize = 15.sp)
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("• 한국관광공사 국문 관광정보 (KorService2)", fontSize = 13.sp)
                    Text("• 한국관광공사 반려동물 동반여행 (KorPetTourService2)", fontSize = 13.sp)
                    Text("• 대한민국 기상청 단기예보 조회서비스", fontSize = 13.sp)
                }
            }

            Text("약관 및 정책", fontWeight = FontWeight.SemiBold, fontSize = 15.sp)
            Card(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("📜 서비스 이용약관", fontSize = 14.sp)
                    Divider()
                    Text("🔒 개인정보 처리방침", fontSize = 14.sp)
                    Divider()
                    Text("⚖️ 오픈소스 라이선스", fontSize = 14.sp)
                }
            }
        }
    }
}
