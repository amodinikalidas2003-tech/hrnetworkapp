package com.hrnetwork.app.form.mapper;

import com.hrnetwork.app.form.dto.FormSchemaDTO;
import com.hrnetwork.app.form.entity.FormSchema;
import com.hrnetwork.app.iam.entity.User;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.UUID;
import javax.annotation.processing.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2026-03-13T22:25:24+0330",
    comments = "version: 1.5.5.Final, compiler: javac, environment: Java 21.0.10 (Microsoft)"
)
@Component
public class FormSchemaMapperImpl implements FormSchemaMapper {

    @Override
    public FormSchemaDTO toDto(FormSchema entity) {
        if ( entity == null ) {
            return null;
        }

        FormSchemaDTO.FormSchemaDTOBuilder formSchemaDTO = FormSchemaDTO.builder();

        formSchemaDTO.createdById( entityCreatedById( entity ) );
        formSchemaDTO.id( entity.getId() );
        formSchemaDTO.name( entity.getName() );
        formSchemaDTO.description( entity.getDescription() );
        Map<String, Object> map = entity.getSchemaDefinition();
        if ( map != null ) {
            formSchemaDTO.schemaDefinition( new LinkedHashMap<String, Object>( map ) );
        }
        formSchemaDTO.createdAt( entity.getCreatedAt() );
        formSchemaDTO.updatedAt( entity.getUpdatedAt() );

        return formSchemaDTO.build();
    }

    @Override
    public FormSchema toEntity(FormSchemaDTO dto) {
        if ( dto == null ) {
            return null;
        }

        FormSchema.FormSchemaBuilder formSchema = FormSchema.builder();

        formSchema.id( dto.getId() );
        formSchema.name( dto.getName() );
        formSchema.description( dto.getDescription() );
        Map<String, Object> map = dto.getSchemaDefinition();
        if ( map != null ) {
            formSchema.schemaDefinition( new LinkedHashMap<String, Object>( map ) );
        }
        formSchema.createdAt( dto.getCreatedAt() );
        formSchema.updatedAt( dto.getUpdatedAt() );

        return formSchema.build();
    }

    private UUID entityCreatedById(FormSchema formSchema) {
        if ( formSchema == null ) {
            return null;
        }
        User createdBy = formSchema.getCreatedBy();
        if ( createdBy == null ) {
            return null;
        }
        UUID id = createdBy.getId();
        if ( id == null ) {
            return null;
        }
        return id;
    }
}
