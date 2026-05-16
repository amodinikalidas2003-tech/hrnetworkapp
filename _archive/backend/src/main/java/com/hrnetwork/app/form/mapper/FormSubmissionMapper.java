package com.hrnetwork.app.form.mapper;

import com.hrnetwork.app.form.dto.FormSubmissionDTO;
import com.hrnetwork.app.form.entity.FormSubmission;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface FormSubmissionMapper {

    @Mapping(source = "schema.id", target = "schemaId")
    @Mapping(source = "submittedBy.id", target = "submittedById")
    FormSubmissionDTO toDto(FormSubmission entity);

    @Mapping(target = "schema", ignore = true)
    @Mapping(target = "submittedBy", ignore = true)
    FormSubmission toEntity(FormSubmissionDTO dto);
}
