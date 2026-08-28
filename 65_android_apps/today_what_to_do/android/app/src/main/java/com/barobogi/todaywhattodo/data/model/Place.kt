package com.barobogi.todaywhattodo.data.model

import com.google.gson.annotations.SerializedName

data class FactCheck(
    @SerializedName("is_verified") val isVerified: Boolean?,
    @SerializedName("confidence_score") val confidenceScore: Double?,
    @SerializedName("verification_notes") val verificationNotes: List<String>?
)

data class WhyCard(
    @SerializedName("title") val title: String,
    @SerializedName("badges") val badges: List<String>?,
    @SerializedName("verified_facts") val verifiedFacts: List<String>?,
    @SerializedName("transparency_note") val transparencyNote: String?
)

data class Place(
    @SerializedName("contentid") val contentId: String,
    @SerializedName("title") val title: String,
    @SerializedName("contenttypeid") val contentTypeId: String?,
    @SerializedName("addr1") val address: String?,
    @SerializedName("mapx") val mapX: String?,
    @SerializedName("mapy") val mapY: String?,
    @SerializedName("tel") val tel: String?,
    @SerializedName("overview") val overview: String?,
    @SerializedName("firstimage") val firstImage: String?,
    @SerializedName("calculated_distance_km") val distanceKm: Double?,
    @SerializedName("final_score") val finalScore: Double?,
    @SerializedName("filter_pass_reasons") val filterPassReasons: List<String>?,
    @SerializedName("fact_check") val factCheck: FactCheck?,
    @SerializedName("detail_intro") val detailIntro: DetailIntro?
)

data class DetailIntro(
    @SerializedName("restdate") val restDate: String?,
    @SerializedName("restdateculture") val restDateCulture: String?,
    @SerializedName("usefee") val useFee: String?,
    @SerializedName("usefeeculture") val useFeeCulture: String?,
    @SerializedName("usetime") val useTime: String?,
    @SerializedName("usetimeculture") val useTimeCulture: String?
)

data class RecommendedCourse(
    @SerializedName("course_name") val courseName: String,
    @SerializedName("places") val places: List<Place>,
    @SerializedName("estimated_duration_hours") val durationHours: Double,
    @SerializedName("summary") val summary: String,
    @SerializedName("ai_reason") val aiReason: String?,
    @SerializedName("why_badges") val whyBadges: List<String>?,
    @SerializedName("why_card") val whyCard: WhyCard?
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
