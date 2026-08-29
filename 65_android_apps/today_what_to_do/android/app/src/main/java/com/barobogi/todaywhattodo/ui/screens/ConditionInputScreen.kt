package com.barobogi.todaywhattodo.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.barobogi.todaywhattodo.ui.theme.PrimaryBlue
import com.barobogi.todaywhattodo.viewmodel.RecommendViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ConditionInputScreen(
    initialCompanion: String,
    viewModel: RecommendViewModel,
    onNavigateToResult: () -> Unit,
    onBack: () -> Unit
) {
    var companion by remember { mutableStateOf(initialCompanion) }
    var customInput by remember { mutableStateOf(viewModel.customCompanionInput) }
    var radiusSlider by remember { mutableStateOf(viewModel.currentRadiusKm.toFloat()) }
    var budgetSlider by remember { mutableStateOf(viewModel.currentBudget.toFloat()) }
    var hoursSlider by remember { mutableStateOf(viewModel.currentHours.toFloat()) }
    var withPet by remember { mutableStateOf(viewModel.withPet) }
    var preferIndoor by remember { mutableStateOf(viewModel.preferIndoor) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("오늘의 조건 입력 🎯", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Text("◀", fontSize = 18.sp)
                    }
                }
            )
        },
        bottomBar = {
            Button(
                onClick = {
                    viewModel.currentCompanion = companion
                    viewModel.customCompanionInput = customInput
                    viewModel.currentRadiusKm = radiusSlider.toDouble()
                    viewModel.currentBudget = budgetSlider.toInt()
                    viewModel.currentHours = hoursSlider.toDouble()
                    viewModel.withPet = withPet
                    viewModel.preferIndoor = preferIndoor
                    viewModel.requestRecommendation()
                    onNavigateToResult()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .height(52.dp),
                shape = RoundedCornerShape(14.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PrimaryBlue)
            ) {
                Text("맞춤 장소 추천받기 🚀", fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 16.dp)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(20.dp)
        ) {
            // 1. 동행자 선택 (세분화 칩)
            Column {
                Text("누구와 함께 가나요? 👥", fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
                Spacer(modifier = Modifier.height(8.dp))
                val companionList = listOf("영유아", "7세 아이", "초등학생", "연인", "반려동물", "부모님", "친구", "혼자")
                LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(companionList) { item ->
                        FilterChip(
                            selected = (companion == item && customInput.isBlank()),
                            onClick = {
                                companion = item
                                customInput = ""
                                if (item == "반려동물") withPet = true
                            },
                            label = { Text(item) }
                        )
                    }
                }
                Spacer(modifier = Modifier.height(10.dp))
                OutlinedTextField(
                    value = customInput,
                    onValueChange = { customInput = it },
                    label = { Text("✍️ 직접 입력 (예: 100일 아기와 시부모님)") },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    singleLine = true
                )
            }

            // 2. 이동 가능 반경 (핫플가이드 벤치마킹)
            Column {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("이동 가능 반경 📍", fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
                    Text("${radiusSlider.toInt()}km 이내", fontWeight = FontWeight.Bold, color = PrimaryBlue)
                }
                Slider(
                    value = radiusSlider,
                    onValueChange = { radiusSlider = it },
                    valueRange = 1f..15f,
                    steps = 13
                )
            }

            // 3. 예산 설정
            Column {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("예산 한도", fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
                    Text("${budgetSlider.toInt() / 10000}만 원 이하", fontWeight = FontWeight.Bold, color = PrimaryBlue)
                }
                Slider(
                    value = budgetSlider,
                    onValueChange = { budgetSlider = it },
                    valueRange = 0f..100000f,
                    steps = 9
                )
            }

            // 4. 가용 시간
            Column {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("활동 가능 시간", fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
                    Text("${hoursSlider.toInt()}시간", fontWeight = FontWeight.Bold, color = PrimaryBlue)
                }
                Slider(
                    value = hoursSlider,
                    onValueChange = { hoursSlider = it },
                    valueRange = 1f..8f,
                    steps = 6
                )
            }

            // 5. 추가 옵션
            Card(
                shape = RoundedCornerShape(14.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("실내 장소만 추천받기 🏛️")
                        Switch(checked = preferIndoor, onCheckedChange = { preferIndoor = it })
                    }
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("반려동물 동반 가능 장소만 🐾")
                        Switch(checked = withPet, onCheckedChange = { withPet = it })
                    }
                }
            }
        }
    }
}
