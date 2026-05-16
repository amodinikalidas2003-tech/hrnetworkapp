package com.hrnetwork.app.dashboard.controller;

import com.hrnetwork.app.common.dto.ApiResponse;
import com.hrnetwork.app.dashboard.dto.HrDashboardStatsDTO;
import com.hrnetwork.app.dashboard.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/dashboard")
@RequiredArgsConstructor
public class DashboardController {

    private final DashboardService dashboardService;

    @GetMapping("/stats")
    public ResponseEntity<ApiResponse<HrDashboardStatsDTO>> getGlobalStats() {
        return ResponseEntity.ok(ApiResponse.success(dashboardService.getGlobalStats()));
    }
}
