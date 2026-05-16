package com.hrnetwork.app.org.controller;

import com.hrnetwork.app.common.dto.ApiResponse;
import com.hrnetwork.app.org.dto.DepartmentDTO;
import com.hrnetwork.app.org.service.DepartmentService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/departments")
@RequiredArgsConstructor
public class DepartmentController {

    private final DepartmentService departmentService;

    @PostMapping
    public ResponseEntity<ApiResponse<DepartmentDTO>> createDepartment(@Valid @RequestBody DepartmentDTO dto) {
        DepartmentDTO created = departmentService.createDepartment(dto);
        return ResponseEntity.ok(ApiResponse.success(created));
    }

    @GetMapping
    public ResponseEntity<ApiResponse<Page<DepartmentDTO>>> getAllDepartments(Pageable pageable) {
        Page<DepartmentDTO> departments = departmentService.getAllDepartments(pageable);
        return ResponseEntity.ok(ApiResponse.success(departments));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<DepartmentDTO>> getDepartmentById(@PathVariable UUID id) {
        DepartmentDTO department = departmentService.getDepartmentById(id);
        return ResponseEntity.ok(ApiResponse.success(department));
    }
}
