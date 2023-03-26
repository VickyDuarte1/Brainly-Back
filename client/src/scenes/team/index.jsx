import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataTeam } from "../../data/mockData";
import AdminPanelSettingsOutlinedIcon from "@mui/icons-material/AdminPanelSettingsOutlined";
import LockOpenOutlinedIcon from "@mui/icons-material/LockOpenOutlined";
import SecurityOutlinedIcon from "@mui/icons-material/SecurityOutlined";
import Header from "../../components/Header";
import { useState, useEffect } from "react";

const Team = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [data, setData] = useState([]);
  const [numItems, setNumItems] = useState(0);
  
  const columns = [
    { field: "id", 
      headerName: "ID", 
      flex: 0.5 
    },
    {
      field: "nombre",
      headerName: "Nombre",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "usuario",
      headerName: "Usuario",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "telefono",
      headerName: "Teléfono",
      flex: 1,
    },
    {
      field: "correo",
      headerName: "Correo",
      flex: 1,
    },
    {
      field: "direccion",
      headerName: "Dirección",
      flex: 1,
    },
    {
      field: "edad",
      headerName: "Edad",
      type: "number",
      headerAlign: "left",
      align: "left",
    },
    {
      field: "fecha_nacimiento",
      headerName: "Fecha de nacimiento",
      type: "date",
      headerAlign: "left",
      align: "left",
      flex: 1,
    },
    {
      field: "genero",
      headerName: "Género",
      flex: 1,
    },
    {
      field: "credenciales",
      headerName: "Credenciales",
      flex: 1,
    },
    {
      field: "especialidad",
      headerName: "Especialidad",
      flex: 1,
    },
    {
      field: "resultado",
      headerName: "Resultado",
      flex: 1,
    },
    {
      field: "imagen",
      headerName: "Imagen",
      flex: 1,
    },
    {
      field: "rol",
      headerName: "Tipo de usuario",
      flex: 1,
      renderCell: ({ row: { access } }) => {
        return (
          <Box
            width="60%"
            m="0 auto"
            p="5px"
            display="flex"
            justifyContent="center"
            backgroundColor={
              access === "admin"
                ? colors.greenAccent[600]
                : access === "Doctor"
                ? colors.greenAccent[700]
                : colors.greenAccent[700]
            }
            borderRadius="4px"
          >
            {access === "admin" && <AdminPanelSettingsOutlinedIcon />}
            {access === "Doctor" && <SecurityOutlinedIcon />}
            {access === "Paciente" && <LockOpenOutlinedIcon />}
            <Typography color={colors.grey[100]} sx={{ ml: "5px" }}>
              {access}
            </Typography>
          </Box>
        );
      },
    },
  ];

  useEffect(() => {
    const fetchContacts = async () => {
      try {
        const [doctoresResponse, pacientesResponse] = await Promise.all([
          fetch("http://localhost:5000/doctores").then((response) =>
            response.json()
          ),
          fetch("http://localhost:5000/pacientes").then((response) =>
            response.json()
          ),
        ]);
        console.log(doctoresResponse, pacientesResponse)
  
        const doctoresData = Array.isArray(doctoresResponse)
          ? doctoresResponse
          : doctoresResponse.doctores;
        const pacientesData = Array.isArray(pacientesResponse)
          ? pacientesResponse
          : pacientesResponse.pacientes;
  
        const transformedData = [
          ...doctoresData.map((doctor) => ({
            id: doctor.id,
            nombre: doctor.nombre,
            correo: doctor.correo,
            usuario: doctor.usuario,
            contraseña: doctor.contraseña,
            imagen: doctor.imagen,
            edad: doctor.edad,
            genero: doctor.genero,
            fecha_nacimiento: doctor.fecha_nacimiento,
            direccion: doctor.direccion,
            telefono: doctor.telefono,
            especialidad: doctor.especialidad,
            credenciales: doctor.credenciales,
            rol: doctor.rol
          })),
          ...pacientesData.map((paciente) => ({
            id: paciente.id,
            nombre: paciente.nombre,
            correo: paciente.correo,
            usuario: paciente.usuario,
            contraseña: paciente.contraseña,
            imagen: paciente.imagen,
            edad: paciente.edad,
            genero: paciente.genero,
            fecha_nacimiento: paciente.fecha_nacimiento,
            direccion: paciente.direccion,
            telefono: paciente.telefono,
            resultado: paciente.resultado,
            rol: paciente.rol
          })),
        ];

        setData(transformedData);
      } catch (error) {
        console.error("Error fetching contacts data:", error);
      }
    };

    fetchContacts();
  }, []);


  return (
    <Box m="20px">
      <Header title="Usuarios totales" subtitle="Listado de registros en la app" />
      <Box
        m="40px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
        }}
      >
        <DataGrid checkboxSelection rows={data} columns={columns} />
      </Box>
    </Box>
  );
};

export default Team;
