package com.hrnetwork.app.org.mapper;

import com.hrnetwork.app.org.dto.DepartmentDTO;
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
public class DepartmentMapperImpl implements DepartmentMapper {

    @Override
    public DepartmentDTO toDto(Department entity) {
        if ( entity == null ) {
            return null;
        }

        DepartmentDTO.DepartmentDTOBuilder departmentDTO = DepartmentDTO.builder();

        departmentDTO.parentId( entityParentId( entity ) );
        departmentDTO.id( entity.getId() );
        departmentDTO.name( entity.getName() );
        departmentDTO.createdAt( entity.getCreatedAt() );
        departmentDTO.updatedAt( entity.getUpdatedAt() );

        return departmentDTO.build();
    }

    @Override
    public Department toEntity(DepartmentDTO dto) {
        if ( dto == null ) {
            return null;
        }

        Department.DepartmentBuilder department = Department.builder();

        department.id( dto.getId() );
        department.name( dto.getName() );
        department.createdAt( dto.getCreatedAt() );
        department.updatedAt( dto.getUpdatedAt() );

        return department.build();
    }

    private UUID entityParentId(Department department) {
        if ( department == null ) {
            return null;
        }
        Department parent = department.getParent();
        if ( parent == null ) {
            return null;
        }
        UUID id = parent.getId();
        if ( id == null ) {
            return null;
        }
        return id;
    }
}
