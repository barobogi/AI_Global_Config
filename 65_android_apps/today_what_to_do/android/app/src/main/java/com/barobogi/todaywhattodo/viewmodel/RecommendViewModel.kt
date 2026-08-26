package com.barobogi.todaywhattodo.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.barobogi.todaywhattodo.data.api.TodayApiService
import com.barobogi.todaywhattodo.data.model.Place
import com.barobogi.todaywhattodo.data.model.RecommendRequest
import com.barobogi.todaywhattodo.data.model.RecommendedCourse
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed interface RecommendUiState {
    object Idle : RecommendUiState
    object Loading : RecommendUiState
    data class Success(
        val topPlaces: List<Place>,
        val courses: List<RecommendedCourse>
    ) : RecommendUiState
    data class Error(val message: String) : RecommendUiState
}

class RecommendViewModel(
    private val apiService: TodayApiService = TodayApiService.create()
) : ViewModel() {

    private val _uiState = MutableStateFlow<RecommendUiState>(RecommendUiState.Idle)
    val uiState: StateFlow<RecommendUiState> = _uiState.asStateFlow()

    // 사용자 입력 조건 상태
    var currentCompanion: String = "7세 아이"
    var currentBudget: Int = 30000
    var currentHours: Double = 3.0
    var withPet: Boolean = false
    var preferIndoor: Boolean = false

    fun requestRecommendation(
        lat: Double = 37.5665,
        lon: Double = 126.9780,
        rainProb: Int = 0
    ) {
        viewModelScope.launch {
            _uiState.value = RecommendUiState.Loading
            try {
                val req = RecommendRequest(
                    lat = lat,
                    lon = lon,
                    max_distance_km = 10.0,
                    budget = currentBudget,
                    with_pet = withPet,
                    companion = currentCompanion,
                    available_hours = currentHours,
                    prefer_indoor = preferIndoor,
                    rain_probability = rainProb
                )
                val resp = apiService.getRecommendations(req)
                if (resp.status == "success" && resp.topPlaces != null) {
                    _uiState.value = RecommendUiState.Success(
                        topPlaces = resp.topPlaces,
                        courses = resp.recommendedCourses ?: emptyList()
                    )
                } else {
                    _uiState.value = RecommendUiState.Error(resp.message ?: "추천 장소를 찾을 수 없습니다.")
                }
            } catch (e: Exception) {
                _uiState.value = RecommendUiState.Error("네트워크 오류: ${e.localizedMessage}")
            }
        }
    }
}
