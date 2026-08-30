package com.barobogi.todaywhattodo

import com.barobogi.todaywhattodo.data.model.NationwideLandmarks
import com.barobogi.todaywhattodo.viewmodel.RecommendViewModel
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class RecommendViewModelTest {

    private val viewModel = RecommendViewModel()

    @Test
    fun testHaversineKmAccuracy() {
        // 서울 종로 (37.5796, 126.9770) -> 부산 해운대 (35.1587, 129.1604)
        val distSeoulToBusan = viewModel.haversineKm(37.5796, 126.9770, 35.1587, 129.1604)
        assertTrue("서울-부산 거리는 약 320km~330km 사이여야 함", distSeoulToBusan in 320.0..330.0)

        // 인천 송도 (37.3925, 126.6394) -> 서울 경복궁 (37.5796, 126.9770)
        val distIncheonToSeoul = viewModel.haversineKm(37.3925, 126.6394, 37.5796, 126.9770)
        assertTrue("인천-서울 거리는 약 35km~40km 사이여야 함", distIncheonToSeoul in 35.0..40.0)
    }

    @Test
    fun testAuthenticLandmarkCoordinates() {
        // 30개 전국 대표 명소 데이터셋 위경도 0.0 초과 무결성 검증
        assertFalse(NationwideLandmarks.ALL.isEmpty())
        for (lm in NationwideLandmarks.ALL) {
            assertTrue("위도는 33~39 사이", lm.lat in 33.0..39.0)
            assertTrue("경도는 125~131 사이", lm.lon in 125.0..131.0)
            assertFalse(lm.name.isBlank())
            assertFalse(lm.address.isBlank())
        }
    }
}
