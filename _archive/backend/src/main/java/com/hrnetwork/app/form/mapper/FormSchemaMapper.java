package com.hrnetwork.app.form.mapper;

import com.hrnetwork.app.form.dto.FormSchemaDTO;
import com.hrnetwork.app.form.entity.FormSchema;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface FormSchemaMapper {

    @Mapping(source = "createdBy.id", target = "createdById")
    FormSchemaDTO toDto(FormSchema entity);

    @Mapping(target = "createdBy", ignore = true) // Will be set by the service layer
    FormSchema toEntity(FormSchemaDTO dto);
}
