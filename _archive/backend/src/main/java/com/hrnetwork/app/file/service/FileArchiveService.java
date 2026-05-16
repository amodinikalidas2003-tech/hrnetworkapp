package com.hrnetwork.app.file.service;

import com.hrnetwork.app.file.entity.FileArchive;
import com.hrnetwork.app.file.repository.FileArchiveRepository;
import com.hrnetwork.app.iam.entity.User;
import com.hrnetwork.app.iam.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class FileArchiveService {

    private final FileArchiveRepository fileRepository;
    private final UserRepository userRepository;

    // Typically you'd use AWS S3, MinIO, or similar. Using local FS for demo.
    private final String uploadDir = "uploads/";

    @Transactional
    public FileArchive uploadFile(MultipartFile file, UUID uploaderId) throws IOException {
        User uploader = userRepository.findById(uploaderId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        // Ensure directory exists
        Path dirPath = Paths.get(uploadDir);
        if (!Files.exists(dirPath)) {
            Files.createDirectories(dirPath);
        }

        String storedFileName = UUID.randomUUID() + "_" + file.getOriginalFilename();
        Path filePath = dirPath.resolve(storedFileName);
        
        Files.copy(file.getInputStream(), filePath);

        FileArchive archive = FileArchive.builder()
                .originalFileName(file.getOriginalFilename())
                .storedFileName(storedFileName)
                .contentType(file.getContentType())
                .size(file.getSize())
                .uploadedBy(uploader)
                .build();

        return fileRepository.save(archive);
    }
}
