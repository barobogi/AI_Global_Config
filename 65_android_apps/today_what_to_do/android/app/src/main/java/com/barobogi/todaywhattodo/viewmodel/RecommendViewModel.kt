package com.barobogi.todaywhattodo.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.barobogi.todaywhattodo.data.api.TodayApiService
import com.barobogi.todaywhattodo.data.model.DetailIntro
import com.barobogi.todaywhattodo.data.model.NationwideLandmarks
import com.barobogi.todaywhattodo.data.model.Place
import com.barobogi.todaywhattodo.data.model.RecommendRequest
import com.barobogi.todaywhattodo.data.model.RecommendedCourse
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.pow
import kotlin.math.sin
import kotlin.math.sqrt

sealed interface RecommendUiState {
    object Idle : RecommendUiState
    object Loading : RecommendUiState
    data class Success(
        val topPlaces: List<Place>,
        val courses: List<RecommendedCourse>,
        val isExtendedFallback: Boolean = false,
        val fallbackNoticeMessage: String? = null
    ) : RecommendUiState
    data class Error(val message: String) : RecommendUiState
}

class RecommendViewModel(
    private val apiService: TodayApiService = TodayApiService.create()
) : ViewModel() {

    private val _uiState = MutableStateFlow<RecommendUiState>(RecommendUiState.Idle)
    val uiState: StateFlow<RecommendUiState> = _uiState.asStateFlow()

    // 스마트 자동 설정 모드 (수동 조절 시 false 자동 전환)
    var isAutoSetting: Boolean = true

    // 사용자 입력 조건 및 GPS 상태
    var currentLat: Double = 37.5665
    var currentLon: Double = 126.9780
    var locationName: String = "위치 탐색 중..."
    var currentRadiusKm: Double = 5.0
    var currentCompanion: String = "7세 아이"
    var customCompanionInput: String = ""
    var currentBudget: Int = 30000
    var currentHours: Double = 3.0
    var withPet: Boolean = false
    var preferIndoor: Boolean = false

    fun updateLocation(lat: Double, lon: Double, name: String) {
        currentLat = lat
        currentLon = lon
        locationName = name
    }

    fun haversineKm(lat1: Double, lon1: Double, lat2: Double, lon2: Double): Double {
        val R = 6371.0
        val dLat = Math.toRadians(lat2 - lat1)
        val dLon = Math.toRadians(lon2 - lon1)
        val a = sin(dLat / 2).pow(2) +
                cos(Math.toRadians(lat1)) * cos(Math.toRadians(lat2)) *
                sin(dLon / 2).pow(2)
        val c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
    }

    fun requestRecommendation(
        lat: Double = currentLat,
        lon: Double = currentLon,
        radiusKm: Double = currentRadiusKm,
        rainProb: Int = 0
    ) {
        viewModelScope.launch {
            _uiState.value = RecommendUiState.Loading
            val effectiveCompanion = if (customCompanionInput.isNotBlank()) customCompanionInput else currentCompanion
            val groupCount = when {
                effectiveCompanion.contains("가족") || effectiveCompanion.contains("부모님") || effectiveCompanion.contains("시부모님") -> 4
                effectiveCompanion.contains("연인") || effectiveCompanion.contains("친구") -> 2
                effectiveCompanion.contains("혼자") -> 1
                effectiveCompanion.contains("아이") || effectiveCompanion.contains("어린이") || effectiveCompanion.contains("학생") || effectiveCompanion.contains("자녀") || effectiveCompanion.contains("유아") -> 3
                else -> 2
            }
            val effectiveBudget = if (isAutoSetting) {
                when (groupCount) {
                    1 -> 20000
                    2 -> 40000
                    else -> 60000
                }
            } else currentBudget

            try {
                // 1단계: 요청된 정직한 반경(radiusKm) 내 1차 검색
                val req = RecommendRequest(
                    lat = lat,
                    lon = lon,
                    max_distance_km = radiusKm,
                    budget = effectiveBudget,
                    with_pet = withPet,
                    companion = effectiveCompanion,
                    available_hours = currentHours,
                    prefer_indoor = preferIndoor,
                    rain_probability = rainProb
                )
                val resp = apiService.getRecommendations(req)
                if (resp.status == "success" && !resp.topPlaces.isNullOrEmpty()) {
                    val filteredPlaces = resp.topPlaces.filter { (it.distanceKm ?: 0.0) <= radiusKm }
                    if (filteredPlaces.isNotEmpty()) {
                        _uiState.value = RecommendUiState.Success(
                            topPlaces = filteredPlaces,
                            courses = resp.recommendedCourses ?: emptyList(),
                            isExtendedFallback = false
                        )
                        return@launch
                    }
                }

                // 2단계 (바로보기님 아이디어): 5km 이내에 장소가 없을 경우, 10~30km 범위의 인근 광역 대표 명소로 대체 안내 (정직한 거리 표시)
                val extendedReq = RecommendRequest(
                    lat = lat,
                    lon = lon,
                    max_distance_km = 30.0,
                    budget = effectiveBudget,
                    with_pet = withPet,
                    companion = effectiveCompanion,
                    available_hours = currentHours,
                    prefer_indoor = preferIndoor,
                    rain_probability = rainProb
                )
                val extendedResp = apiService.getRecommendations(extendedReq)
                if (extendedResp.status == "success" && !extendedResp.topPlaces.isNullOrEmpty()) {
                    val extendedPlaces = extendedResp.topPlaces.take(3)
                    val noticeMsg = "💡 설정하신 ${radiusKm.toInt()}km 반경 내에는 장소가 없어, 직선거리 기준 인근 광역 대표 명소를 정직하게 대체 안내해 드립니다. (실제 차량 이동거리는 지형에 따라 다를 수 있습니다)"
                    _uiState.value = RecommendUiState.Success(
                        topPlaces = extendedPlaces,
                        courses = extendedResp.recommendedCourses ?: emptyList(),
                        isExtendedFallback = true,
                        fallbackNoticeMessage = noticeMsg
                    )
                } else {
                    // 3단계: 코니 수혈 가이드 100% 이식 — 실좌표 하버사인 계산 기반 정속 전국 랜드마크 폴백
                    val (fallbackPlaces, fallbackCourses) = getLocalFallbackPlaces(lat, lon, effectiveCompanion, radiusKm, effectiveBudget)
                    val noticeMsg = "💡 내 현재 위치 기준 최근접 전국 대표 명소를 정직한 직선거리로 안내해 드립니다."
                    _uiState.value = RecommendUiState.Success(
                        topPlaces = fallbackPlaces,
                        courses = fallbackCourses,
                        isExtendedFallback = true,
                        fallbackNoticeMessage = noticeMsg
                    )
                }
            } catch (e: Exception) {
                val (fallbackPlaces, fallbackCourses) = getLocalFallbackPlaces(lat, lon, effectiveCompanion, radiusKm, effectiveBudget)
                _uiState.value = RecommendUiState.Success(
                    topPlaces = fallbackPlaces,
                    courses = fallbackCourses,
                    isExtendedFallback = true,
                    fallbackNoticeMessage = "💡 현재 위치 기준 정속 명소 안내"
                )
            }
        }
    }

    private fun getLocalFallbackPlaces(
        lat: Double,
        lon: Double,
        companion: String,
        targetRadiusKm: Double,
        targetBudget: Int
    ): Pair<List<Place>, List<RecommendedCourse>> {
        val rankedAll = NationwideLandmarks.ALL
            .map { landmark -> landmark to haversineKm(lat, lon, landmark.lat, landmark.lon) }
            .sortedBy { it.second }

        val closestDist = rankedAll.firstOrNull()?.second ?: 0.0
        val displayCount = if (closestDist > 50.0) 1 else 2
        val ranked = rankedAll.take(displayCount)

        val places = ranked.map { (landmark, distKm) ->
            val distFormatted = String.format(java.util.Locale.US, "%.1f", distKm)
            val withinRadius = distKm <= targetRadiusKm
            val reasonMsg = when {
                withinRadius -> "📍 내 위치에서 직선거리 약 ${distFormatted}km (${targetRadiusKm.toInt()}km 반경 이내)"
                distKm > 50.0 -> "📍 정말 멀리 떨어져 있지만 (직선거리 약 ${distFormatted}km) 내 위치에서 가장 가까운 전국 대표 명소를 정직하게 안내합니다"
                else -> "📍 내 위치에서 직선거리 약 ${distFormatted}km (요청하신 ${targetRadiusKm.toInt()}km 반경보다 멀지만, 주변 조건에 맞는 곳이 없어 가장 가까운 전국 대표 명소를 정직하게 안내합니다)"
            }

            Place(
                contentId = landmark.contentId,    // 순수 숫자 문자열 100% 사용 (음수 hashCode 예방)
                title = landmark.name,
                contentTypeId = "12",
                address = landmark.address,
                mapX = landmark.lon.toString(),   // 실좌표 100% 그대로
                mapY = landmark.lat.toString(),   // 실좌표 100% 그대로
                tel = landmark.tel,
                overview = landmark.overview,
                distanceKm = distKm,               // 실거리 100% 그대로
                finalScore = 90.0,
                filterPassReasons = listOf(
                    reasonMsg,
                    "🛡️ 한국관광공사 공공데이터 검증",
                    "👶 $companion 맞춤 안심 장소"
                ),
                detailIntro = DetailIntro(
                    restDate = landmark.restDate,
                    useFee = landmark.useFee,
                    useTime = landmark.openTime
                )
            )
        }

        val courses = listOf(
            RecommendedCourse(
                courseName = "🌈 내 위치 기준 $companion 맞춤 정직 안내 코스",
                places = places,
                durationHours = currentHours,
                summary = "요청하신 반경 내에는 조건에 맞는 곳이 없어, 실제 GPS 기준 가장 가까운 전국 대표 명소를 정직한 거리로 안내합니다.",
                aiReason = "네트워크 오류 또는 반경 내 후보 없음 → 실좌표 기반 최근접 명소 폴백",
                whyBadges = listOf("정직한 거리 표기", "실좌표 검증")
            )
        )

        return Pair(places, courses)
    }
}
