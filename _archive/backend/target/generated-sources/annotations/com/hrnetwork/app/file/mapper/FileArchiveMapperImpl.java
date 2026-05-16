package com.hrnetwork.app.file.mapper;

import com.hrnetwork.app.file.dto.FileArchiveDTO;
import com.hrnetwork.app.file.entity.FileArchive;
import com.hrnetwork.app.iam.entity.User;
import java.util.UUID;
import javax.annotation.processing.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2026-03-13T22:25:24+0330",
    comments = "version: 1.5.5.Final, compiler: javac, environment: Java 21.0.10 (Microsoft)"
)
@Component
public class FileArchiveMapperImpl implements FileArchiveMapper {

    @Override
    public FileArchiveDTO toDto(FileArchive entity) {
        if ( entity == null ) {
            return null;
        }

        FileArchiveDTO.FileArchiveDTOBuilder fileArchiveDTO = FileArchiveDTO.builder();

        fileArchiveDTO.uploadedById( entityUploadedById( entity ) );
        fileArchiveDTO.id( entity.getId() );
        fileArchiveDTO.originalFileName( entity.getOriginalFileName() );
        fileArchiveDTO.contentType( entity.getContentType() );
        fileArchiveDTO.size( entity.getSize() );
        fileArchiveDTO.createdAt( entity.getCreatedAt() );

        return fileArchiveDTO.build();
    }

    @Override
    public FileArchive toEntity(FileArchiveDTO dto) {
        if ( dto == null ) {
            return null;
        }

        FileArchive.FileArchiveBuilder fileArchive = FileArchive.builder();

        fileArchive.id( dto.getId() );
        fileArchive.originalFileName( dto.getOriginalFileName() );
        fileArchive.contentType( dto.getContentType() );
        fileArchive.size( dto.getSize() );
        fileArchive.createdAt( dto.getCreatedAt() );

        return fileArchive.build();
    }

    private UUID entityUploadedById(FileArchive fileArchive) {
        if ( fileArchive == null ) {
            return null;
        }
        User uploadedBy = fileArchive.getUploadedBy();
        if ( uploadedBy == null ) {
            return null;
        }
        UUID id = uploadedBy.getId();
        if ( id == null ) {
            return null;
        }
        return id;
    }
}
