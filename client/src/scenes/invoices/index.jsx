import { Box } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
// import { mockDataContacts } from "../../data/mockData";
import Header from "../../components/Header";
import { useTheme } from "@mui/material";
import { useState, useEffect } from "react";


const Invoices = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

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
      field: "imagen",
      headerName: "Imagen",
      flex: 1,
    },
  ];

  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/doctores")
      .then((response) => response.json())
      .then((jsonData) => {
        const data = Array.isArray(jsonData) ? jsonData : jsonData.doctores;
        // Transformar los datos obtenidos en el formato esperado por la tabla
        const transformedData = data.map((user) => ({
          id: user.id,
          nombre: user.nombre,
          correo: user.correo,
          usuario: user.usuario,
          contraseña: user.contraseña,
          imagen: user.imagen,
          edad: user.edad,
          genero: user.genero,
          fecha_nacimiento: user.fecha_nacimiento,
          direccion: user.direccion,
          telefono: user.telefono,
          especialidad: user.especialidad,
          credenciales: user.credenciales
        }));
        setData(transformedData);
      })
      .catch((error) => console.error("Error fetching users data:", error));
  }, []);



  return (
    <Box m="20px">
      <Header
        title="DOCTORES"
        subtitle="Listado de doctores"
      />
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
          "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
            color: `${colors.grey[100]} !important`,
          },
        }}
      >
        <DataGrid
          rows={data}
          columns={columns}
          components={{ Toolbar: GridToolbar }}
        />
      </Box>
    </Box>
  );
};

export default Invoices;
