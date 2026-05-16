package com.hrnetwork.app.org.mapper;

import com.hrnetwork.app.org.dto.DepartmentDTO;
import com.hrnetwork.app.org.entity.Department;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface DepartmentMapper {

    @Mapping(source = "parent.id", target = "parentId")
    DepartmentDTO toDto(Department entity);

    @Mapping(target = "parent", ignore = true)
    @Mapping(target = "subDepartments", ignore = true)
    @Mapping(target = "users", ignore = true)
    Department toEntity(DepartmentDTO dto);
}
