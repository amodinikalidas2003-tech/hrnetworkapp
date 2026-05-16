package com.hrnetwork.app.file.controller;

import com.hrnetwork.app.common.dto.ApiResponse;
import com.hrnetwork.app.file.dto.FileArchiveDTO;
import com.hrnetwork.app.file.mapper.FileArchiveMapper;
import com.hrnetwork.app.file.service.FileArchiveService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/files")
@RequiredArgsConstructor
public class FileArchiveController {

    private final FileArchiveService fileService;
    private final FileArchiveMapper fileMapper;

    @PostMapping("/upload")
    public ResponseEntity<ApiResponse<FileArchiveDTO>> uploadFile(
            @RequestParam("file") MultipartFile file,
            @RequestParam("uploaderId") UUID uploaderId) {
        
        try {
            var archive = fileService.uploadFile(file, uploaderId);
            return ResponseEntity.ok(ApiResponse.success(fileMapper.toDto(archive)));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }
}
