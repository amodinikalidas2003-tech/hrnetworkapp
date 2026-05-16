package com.hrnetwork.app.iam.mapper;

import com.hrnetwork.app.iam.dto.UserDTO;
import com.hrnetwork.app.iam.entity.User;
import com.hrnetwork.app.org.entity.Department;
import java.util.UUID;
import javax.annotation.processing.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2026-03-13T22:25:24+0330",
    comments = "version: 1.5.5.Final, compiler: javac, environment: Java 21.0.10 (Microsoft)"
)
@Component
public class UserMapperImpl implements UserMapper {

    @Override
    public UserDTO toDto(User entity) {
        if ( entity == null ) {
            return null;
        }

        UserDTO.UserDTOBuilder userDTO = UserDTO.builder();

        userDTO.departmentId( entityDepartmentId( entity ) );
        userDTO.id( entity.getId() );
        userDTO.username( entity.getUsername() );
        userDTO.email( entity.getEmail() );
        userDTO.role( entity.getRole() );
        userDTO.createdAt( entity.getCreatedAt() );
        userDTO.updatedAt( entity.getUpdatedAt() );

        return userDTO.build();
    }

    @Override
    public User toEntity(UserDTO dto) {
        if ( dto == null ) {
            return null;
        }

        User.UserBuilder user = User.builder();

        user.id( dto.getId() );
        user.username( dto.getUsername() );
        user.email( dto.getEmail() );
        user.role( dto.getRole() );
        user.createdAt( dto.getCreatedAt() );
        user.updatedAt( dto.getUpdatedAt() );

        return user.build();
    }

    private UUID entityDepartmentId(User user) {
        if ( user == null ) {
            return null;
        }
        Department department = user.getDepartment();
        if ( department == null ) {
            return null;
        }
        UUID id = department.getId();
        if ( id == null ) {
            return null;
        }
        return id;
    }
}
