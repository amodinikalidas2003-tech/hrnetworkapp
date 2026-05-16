package com.hrnetwork.app.iam.mapper;

import com.hrnetwork.app.iam.dto.UserDTO;
import com.hrnetwork.app.iam.entity.User;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface UserMapper {

    @Mapping(source = "department.id", target = "departmentId")
    UserDTO toDto(User entity);

    @Mapping(target = "password", ignore = true)
    @Mapping(target = "department", ignore = true)
    User toEntity(UserDTO dto);
}
