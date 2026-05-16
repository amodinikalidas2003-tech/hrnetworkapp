package com.hrnetwork.app.form.mapper;

import com.hrnetwork.app.form.dto.FormSubmissionDTO;
import com.hrnetwork.app.form.entity.FormSchema;
import com.hrnetwork.app.form.entity.FormSubmission;
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
public class FormSubmissionMapperImpl implements FormSubmissionMapper {

    @Override
    public FormSubmissionDTO toDto(FormSubmission entity) {
        if ( entity == null ) {
            return null;
        }

        FormSubmissionDTO.FormSubmissionDTOBuilder formSubmissionDTO = FormSubmissionDTO.builder();

        formSubmissionDTO.schemaId( entitySchemaId( entity ) );
        formSubmissionDTO.submittedById( entitySubmittedById( entity ) );
        formSubmissionDTO.id( entity.getId() );
        Map<String, Object> map = entity.getData();
        if ( map != null ) {
            formSubmissionDTO.data( new LinkedHashMap<String, Object>( map ) );
        }
        formSubmissionDTO.createdAt( entity.getCreatedAt() );
        formSubmissionDTO.updatedAt( entity.getUpdatedAt() );

        return formSubmissionDTO.build();
    }

    @Override
    public FormSubmission toEntity(FormSubmissionDTO dto) {
        if ( dto == null ) {
            return null;
        }

        FormSubmission.FormSubmissionBuilder formSubmission = FormSubmission.builder();

        formSubmission.id( dto.getId() );
        Map<String, Object> map = dto.getData();
        if ( map != null ) {
            formSubmission.data( new LinkedHashMap<String, Object>( map ) );
        }
        formSubmission.createdAt( dto.getCreatedAt() );
        formSubmission.updatedAt( dto.getUpdatedAt() );

        return formSubmission.build();
    }

    private UUID entitySchemaId(FormSubmission formSubmission) {
        if ( formSubmission == null ) {
            return null;
        }
        FormSchema schema = formSubmission.getSchema();
        if ( schema == null ) {
            return null;
        }
        UUID id = schema.getId();
        if ( id == null ) {
            return null;
        }
        return id;
    }

    private UUID entitySubmittedById(FormSubmission formSubmission) {
        if ( formSubmission == null ) {
            return null;
        }
        User submittedBy = formSubmission.getSubmittedBy();
        if ( submittedBy == null ) {
            return null;
        }
        UUID id = submittedBy.getId();
        if ( id == null ) {
            return null;
        }
        return id;
    }
}
