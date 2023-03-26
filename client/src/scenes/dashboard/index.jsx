import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import { mockTransactions } from "../../data/mockData";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import EmailIcon from "@mui/icons-material/Email";
import PointOfSaleIcon from "@mui/icons-material/PointOfSale";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import TrafficIcon from "@mui/icons-material/Traffic";
import Header from "../../components/Header";
import LineChart from "../../components/LineChart";
import GeographyChart from "../../components/GeographyChart";
import BarChart from "../../components/BarChart";
import StatBox from "../../components/StatBox";
import ProgressCircle from "../../components/ProgressCircle";
import { useState, useEffect } from "react";

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [data, setData] = useState([]);

  
  // Variable de estado para guardar el número de elementos
  const [numElements, setNumElements] = useState(0);

  console.log(numElements)
  useEffect(() => {
    fetch("http://localhost:5000/doctores")
      .then((response) => response.json())
      .then((jsonData) => {
        const data = Array.isArray(jsonData) ? jsonData : jsonData.doctores;
        // Transformar los datos obtenidos en el formato esperado por la tabla
        const transformedData = data.map((user) => ({
          id: user.id,
        }));
        // Obtener el número de elementos en transformedData
        const numElements = transformedData.length;
        // Asignar los datos transformados a la variable de estado
        setData(transformedData);
        // Asignar el número de elementos a la variable de estado
        setNumElements(numElements);
      })
      .catch((error) => console.error("Error fetching users data:", error));
  }, []);
  
     console.log(numElements)



     
  // Declarar la variable para guardar los últimos 5 usuarios
  const [fiveLastUsers, setFiveLastUsers] = useState([]);
  // Variable de estado para guardar el número de elementos
  const [numElements1, setNumElements1] = useState(0);
  // Variables de estado para guardar el número de usuarios femeninos y masculinos
  const [numFemales, setNumFemales] = useState(0);
  const [numMales, setNumMales] = useState(0);

  useEffect(() => {
    fetch("http://localhost:5000/pacientes")
      .then((response) => response.json())
      .then((jsonData) => {
        const data = Array.isArray(jsonData) ? jsonData : jsonData.pacientes;
        // Transformar los datos obtenidos en el formato esperado por la tabla
        const transformedDatas = data.map((user) => ({
          id: user.id,
          genero: user.genero,
          nombre: user.nombre,
          usuario: user.usuario,
          correo: user.correo,
          telefono: user.telefono
        }));
        // Ordenar los datos en orden descendente según el valor de la propiedad id
        transformedDatas.sort((a, b) => b.id - a.id);
        // Obtener solamente los primeros 5 elementos
        const lastFiveUsers = transformedDatas.slice(0, 5);
        // Mapear los datos de los últimos 5 usuarios a un nuevo array
        setFiveLastUsers(lastFiveUsers.map((user) => ({
          nombre: user.nombre,
          usuario: user.usuario,
          correo: user.correo,
          telefono: user.telefono
        })));
        // Obtener el número de elementos en transformedData
        const numElements1 = transformedDatas.length;
        // Asignar los datos transformados a la variable de estado
        setData(transformedDatas);
        // Asignar el número de elementos a la variable de estado
        setNumElements1(numElements1);
        // Obtener el número de usuarios femeninos
        const numFemales = transformedDatas.filter((user) => user.genero === 'femenino').length;
        // Asignar el número de usuarios femeninos a la variable de estado
        setNumFemales(numFemales);
        // Obtener el número de usuarios masculinos
        const numMales = transformedDatas.filter((user) => user.genero === 'masculino').length;
        // Asignar el número de usuarios masculinos a la variable de estado
        setNumMales(numMales);
      })
      .catch((error) => console.error("Error fetching users data:", error));
  }, []);
    
    console.log(numElements1);
    console.log(fiveLastUsers);
    console.log(numMales, "hombres");
    console.log(numFemales, "mujeres");






  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="DASHBOARD" subtitle="Bienvenido a tu dashboard" />

        <Box>
          <Button
            sx={{
              backgroundColor: colors.blueAccent[700],
              color: colors.grey[100],
              fontSize: "14px",
              fontWeight: "bold",
              padding: "10px 20px",
            }}
          >
            <DownloadOutlinedIcon sx={{ mr: "10px" }} />
            Descargar reportes
          </Button>
        </Box>
      </Box>

      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="140px"
        gap="20px"
      >
        {/* ROW 1 */}
        <Box
          gridColumn="span 6"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={numElements}
            subtitle="Número de doctores registrados"
            progress="0.1"
            increase={`+${numElements}%`}
            icon={
              <EmailIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        <Box
          gridColumn="span 6"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={numElements1}
            subtitle="Número de pacientes registrados"
            progress="0.1"
            increase={`+${numElements1}%`}
            icon={
              <PointOfSaleIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        
        {/* ROW 2 */}
        <Box
          gridColumn="span 8"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Box
            mt="25px"
            p="0 30px"
            display="flex "
            justifyContent="space-between"
            alignItems="center"
          >
            <Box>
              <Typography
                variant="h5"
                fontWeight="600"
                color={colors.grey[100]}
              >
                Revenue Generated
              </Typography>
              <Typography
                variant="h3"
                fontWeight="bold"
                color={colors.greenAccent[500]}
              >
                $59,342.32
              </Typography>
            </Box>
            <Box>
              <IconButton>
                <DownloadOutlinedIcon
                  sx={{ fontSize: "26px", color: colors.greenAccent[500] }}
                />
              </IconButton>
            </Box>
          </Box>
          <Box height="250px" m="-20px 0 0 0">
            <LineChart isDashboard={true} />
          </Box>
        </Box>
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          overflow="auto"
        >
          <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
            borderBottom={`4px solid ${colors.primary[500]}`}
            colors={colors.grey[100]}
            p="15px"
          >
            <Typography color={colors.grey[100]} variant="h5" fontWeight="600">
              Últimos registros
            </Typography>
          </Box>
          {fiveLastUsers.map((user, i) => (
            <Box
              key={`${user.id}-${i}`}
              display="flex"
              justifyContent="space-between"
              alignItems="center"
              borderBottom={`4px solid ${colors.primary[500]}`}
              p="15px"
            >
              <Box>
                <Typography
                  color={colors.greenAccent[500]}
                  variant="h5"
                  fontWeight="600"
                >
                  {user.nombre}
                </Typography>
                <Typography color={colors.grey[100]}>
                  {user.usuario}
                </Typography>
              </Box>
              <Box color={colors.grey[100]}>{user.correo}</Box>
              <Box
                backgroundColor={colors.greenAccent[500]}
                p="5px 10px"
                borderRadius="4px"
              >
                Tel: {user.telefono}
              </Box>
            </Box>
          ))}
        </Box>

        {/* ROW 3 */}
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          p="30px"
        >
          <Typography variant="h5" fontWeight="600">
            No sé qué más poner
          </Typography>
          <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            mt="25px"
          >
            <ProgressCircle size="125" />
            <Typography
              variant="h5"
              color={colors.greenAccent[500]}
              sx={{ mt: "15px" }}
            >
              $48,352 revenue generated
            </Typography>
            <Typography>Includes extra misc expenditures and costs</Typography>
          </Box>
        </Box>
        
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            Pacientes por género
          </Typography>
          <Box height="250px" mt="-20px">
            <BarChart numFemales={numFemales} numMales={numMales} isDashboard={true} />
          </Box>
        </Box>
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          padding="30px"
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ marginBottom: "15px" }}
          >
            Geography Based Traffic
          </Typography>
          <Box height="200px">
            <GeographyChart isDashboard={true} />
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
