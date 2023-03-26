import { Box, Button, Dialog, DialogTitle, DialogContent } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import { useTheme } from "@mui/material";
import { useState, useEffect } from "react";
import Modificar from "../form/modificar";

const Contacts = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const columns = [
    { field: "id", headerName: "ID", flex: 0.3 },
    {
      field: "nombre",
      headerName: "Nombre",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "correo",
      headerName: "Email",
      flex: 1,
    },
    {
      field: "usuario",
      headerName: "Usuario",
      flex: 1,
    },
    {
      field: "contraseña",
      headerName: "Contraseña",
      flex: 1,
    },
    {
      field: "imagen",
      headerName: "Imágen",
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
      field: "genero",
      headerName: "Género",
      flex: 1,
    },
    {
      field: "fecha_nacimiento",
      headerName: "Fecha de Nacimiento",
      flex: 1,
    },
    {
      field: "direccion",
      headerName: "Dirección",
      flex: 1,
    },
    {
      field: "telefono",
      headerName: "Teléfono",
      flex: 1,
    },
    {
      field: "resultado",
      headerName: "Resultado",
      flex: 1,
    },
    {
      field: "acciones",
      headerName: "Modificar",
      flex: 1,
      renderCell: (params) => (
        <Button
          variant="contained"
          color="primary"
          onClick={() => handleModificar(params.id)}
          style={{ backgroundColor: colors.greenAccent[600] }}
        >
          Modificar
        </Button>
      ),
    },
    {
      field: "activo",
      headerName: "Desactivar",
      flex: 1,
      renderCell: (params) => (
        <Button
          variant="contained"
          color="secondary"
          onClick={() => handleDeshabilitar(params.id)}
          style={{ backgroundColor: colors.redAccent[600] }}
          disabled={!params.value}
        >
          Deshabilitar
        </Button>
      ),
    },
    {
      field: "desactivo",
      headerName: "Activar",
      flex: 1,
      renderCell: (params) => (
        <Button
          variant="contained"
          color="secondary"
          onClick={() => handleHabilitar(params.id)}
          style={{ backgroundColor: colors.blueAccent[600] }}
          disabled={!params.value}
        >
          Habilitar
        </Button>
      ),
    },
  ];

  const [data, setData] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [currentPatient, setCurrentPatient] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/pacientes")
      .then((response) => response.json())
      .then((jsonData) => {
        const data = Array.isArray(jsonData) ? jsonData : jsonData.pacientes;
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
          resultado: user.resultado,
          activo: true,
          desactivo: true,
        }));
        setData(transformedData);
      })
      .catch((error) => console.error(error));
  }, []);

  const handleModificar = (id) => {
    // Buscar el paciente por ID
    const patient = data.find((patient) => patient.id === id);
    if (patient) {
      // Establecer el paciente actual y abrir el diálogo
      setCurrentPatient(patient);
      setOpenDialog(true);
    }
  };

  const handleDeshabilitar = (id) => {
    // Enviar una petición PUT al servidor para deshabilitar el usuario
    fetch(`http://localhost:5000/pacientes/${id}/deshabilitar`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ activo: false }),
    })
      .then((response) => response.json())
      .then((jsonData) => {
        // Actualizar la tabla para reflejar el cambio
        setData((prevData) =>
          prevData.map((patient) =>
            patient.id === id ? { ...patient, activo: false } : patient
          )
        );
      })
      .catch((error) => console.error(error));
  };

  const handleHabilitar = (id) => {
    // Enviar una petición PUT al servidor para deshabilitar el usuario
    fetch(`http://localhost:5000/pacientes/${id}/habilitar`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ desactivo: true }),
    })
      .then((response) => response.json())
      .then((jsonData) => {
        // Actualizar la tabla para reflejar el cambio
        setData((prevData) =>
          prevData.map((patient) =>
            patient.id === id ? { ...patient, activo: true } : patient
          )
        );
      })
      .catch((error) => console.error(error));
  };

  const handleCloseDialog = () => {
    // Cerrar el diálogo y restablecer el paciente actual
    setOpenDialog(false);
    setCurrentPatient(null);
  };

  const handleFormSubmit = (newPatientData) => {
    // Enviar los nuevos datos al servidor y actualizar la tabla
    fetch(`http://localhost:5000/pacientes/${currentPatient.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newPatientData),
    })
      .then((response) => response.json())
      .then((jsonData) => {
        const updatedPatient = {
          id: jsonData.id,
          nombre: jsonData.nombre,
          correo: jsonData.correo,
          usuario: jsonData.usuario,
          contraseña: jsonData.contraseña,
          imagen: jsonData.imagen,
          edad: jsonData.edad,
          genero: jsonData.genero,
          fecha_nacimiento: jsonData.fecha_nacimiento,
          direccion: jsonData.direccion,
          telefono: jsonData.telefono,
          resultado: jsonData.resultado,
        };
        // Actualizar la tabla con los nuevos datos
        setData((prevData) => {
          const index = prevData.findIndex(
            (patient) => patient.id === updatedPatient.id
          );
          if (index === -1) {
            return prevData;
          } else {
            const newData = [...prevData];
            newData[index] = updatedPatient;
            return newData;
          }
        });
        // Cerrar el diálogo y restablecer el paciente actual
        setOpenDialog(false);
        setCurrentPatient(null);
      })
      .catch((error) => console.error(error));
  };

  return (
    <Box m="20px">
      <Header title="Pacientes" subtitle="Lista de Pacientes" />
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
      {currentPatient && (
        <Dialog open={openDialog} onClose={handleCloseDialog}>
          <DialogTitle>Modificar paciente</DialogTitle>
          <DialogContent>
            <Modificar patient={currentPatient} onSubmit={handleFormSubmit} />
          </DialogContent>
        </Dialog>
      )}
    </Box>
  );
};

export default Contacts;
