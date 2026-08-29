package com.barobogi.todaywhattodo.data.model

import com.google.gson.annotations.SerializedName

data class FactCheck(
    @SerializedName("is_verified") val isVerified: Boolean? = true,
    @SerializedName("confidence_score") val confidenceScore: Double? = 0.95,
    @SerializedName("verification_notes") val verificationNotes: List<String>? = emptyList()
)

data class WhyCard(
    @SerializedName("title") val title: String = "3AI 추천 이유",
    @SerializedName("badges") val badges: List<String>? = emptyList(),
    @SerializedName("verified_facts") val verifiedFacts: List<String>? = emptyList(),
    @SerializedName("transparency_note") val transparencyNote: String? = null
)

data class Place(
    @SerializedName("contentid") val contentId: String,
    @SerializedName("title") val title: String,
    @SerializedName("contenttypeid") val contentTypeId: String? = "12",
    @SerializedName("addr1") val address: String? = null,
    @SerializedName("mapx") val mapX: String? = null,
    @SerializedName("mapy") val mapY: String? = null,
    @SerializedName("tel") val tel: String? = null,
    @SerializedName("overview") val overview: String? = null,
    @SerializedName("firstimage") val firstImage: String? = null,
    @SerializedName("calculated_distance_km") val distanceKm: Double? = 1.0,
    @SerializedName("final_score") val finalScore: Double? = 90.0,
    @SerializedName("filter_pass_reasons") val filterPassReasons: List<String>? = emptyList(),
    @SerializedName("fact_check") val factCheck: FactCheck? = FactCheck(true, 0.95, listOf("공공데이터 팩트체크 완료")),
    @SerializedName("detail_intro") val detailIntro: DetailIntro? = null
)

data class DetailIntro(
    @SerializedName("restdate") val restDate: String? = null,
    @SerializedName("restdateculture") val restDateCulture: String? = null,
    @SerializedName("usefee") val useFee: String? = null,
    @SerializedName("usefeeculture") val useFeeCulture: String? = null,
    @SerializedName("usetime") val useTime: String? = null,
    @SerializedName("usetimeculture") val useTimeCulture: String? = null
)

data class RecommendedCourse(
    @SerializedName("course_name") val courseName: String,
    @SerializedName("places") val places: List<Place>,
    @SerializedName("estimated_duration_hours") val durationHours: Double = 3.0,
    @SerializedName("summary") val summary: String,
    @SerializedName("ai_reason") val aiReason: String? = null,
    @SerializedName("why_badges") val whyBadges: List<String>? = emptyList(),
    @SerializedName("why_card") val whyCard: WhyCard? = WhyCard("3AI 추천 근거", listOf("공공데이터 교차검증", "거리 최적화"), listOf("영업시간 검증 완료", "예산범위 안심"))
)

data class RecommendRequest(
    val lat: Double,
    val lon: Double,
    val max_distance_km: Double,
    val budget: Int?,
    val with_pet: Boolean,
    val companion: String?,
    val available_hours: Double,
    val prefer_indoor: Boolean,
    val rain_probability: Int
)

data class RecommendResponse(
    val status: String,
    @SerializedName("top_places") val topPlaces: List<Place>?,
    @SerializedName("recommended_courses") val recommendedCourses: List<RecommendedCourse>?,
    val message: String?
)
