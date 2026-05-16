package com.hrnetwork.app.file.mapper;

import com.hrnetwork.app.file.dto.FileArchiveDTO;
import com.hrnetwork.app.file.entity.FileArchive;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface FileArchiveMapper {

    @Mapping(source = "uploadedBy.id", target = "uploadedById")
    FileArchiveDTO toDto(FileArchive entity);

    @Mapping(target = "uploadedBy", ignore = true)
    FileArchive toEntity(FileArchiveDTO dto);
}
