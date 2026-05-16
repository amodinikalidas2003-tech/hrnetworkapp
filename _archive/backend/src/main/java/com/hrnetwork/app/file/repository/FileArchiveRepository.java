package com.hrnetwork.app.file.repository;

import com.hrnetwork.app.file.entity.FileArchive;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface FileArchiveRepository extends JpaRepository<FileArchive, UUID> {
}
