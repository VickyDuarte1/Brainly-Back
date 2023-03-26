import { Box, Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import Header from "../../components/Header";

const Modificar = () => {
  const isNonMobile = useMediaQuery("(min-width:600px)");

  const handleFormSubmit = async (values) => {
    try {
      const response = await fetch(
        `http://localhost:5000/pacientes/${values.id}`,
        {
          method: "PUT", // cambiar a método PUT
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        }
      );

      if (!response.ok) {
        throw new Error("Error al guardar el usuario");
      }

      alert("Usuario Modificado");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Box m="20px">
      <Header
        title="MODIFICAR USUARIO"
        subtitle="Llene los datos a modificar"
      />

      <Formik
        onSubmit={handleFormSubmit}
        initialValues={initialValues}
        validationSchema={checkoutSchema}
      >
        {({
          values,
          errors,
          touched,
          handleBlur,
          handleChange,
          handleSubmit,
        }) => (
          <form onSubmit={handleSubmit}>
            <Box
              display="grid"
              gap="30px"
              gridTemplateColumns="repeat(4, minmax(0, 1fr))"
              sx={{
                "& > div": { gridColumn: isNonMobile ? undefined : "span 4" },
              }}
            >
              <TextField
                fullWidth
                variant="filled"
                type="number"
                label="ID"
                placeholder="ID para modificar"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.id}
                name="id"
                error={!!touched.id && !!errors.id}
                helperText={touched.id && errors.id}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Tipo de Usuario"
                placeholder="Debe seleccionar 'paciente' o 'doctor'"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.tipo_usuario.toLowerCase()}
                name="tipo_usuario"
                error={!!touched.tipo_usuario && !!errors.tipo_usuario}
                helperText={touched.tipo_usuario && errors.tipo_usuario}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Nombre y Apellido"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.nombre}
                name="nombre"
                error={!!touched.nombre && !!errors.nombre}
                helperText={touched.nombre && errors.nombre}
                sx={{ gridColumn: "span 2" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="email"
                label="Correo Electrónico"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.correo}
                name="correo"
                error={!!touched.correo && !!errors.correo}
                helperText={touched.correo && errors.correo}
                sx={{ gridColumn: "span 2" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Nombre de Usuario"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.usuario.toLowerCase()}
                name="usuario"
                error={!!touched.usuario && !!errors.usuario}
                helperText={touched.usuario && errors.usuario}
                sx={{ gridColumn: "span 2" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="password"
                label="Contraseña"
                placeholder="La contraseña debe tener al menos 8 caracteres, una letra minúscula, una letra mayúscula, un número y un carácter especial"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.contraseña}
                name="contraseña"
                error={!!touched.contraseña && !!errors.contraseña}
                helperText={touched.contraseña && errors.contraseña}
                sx={{ gridColumn: "span 2" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="file"
                label="Imágen de Perfil"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.imagen}
                name="imagen"
                error={!!touched.imagen && !!errors.imagen}
                helperText={touched.imagen && errors.imagen}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="number"
                label="Edad"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.edad}
                name="edad"
                error={!!touched.edad && !!errors.edad}
                helperText={touched.edad && errors.edad}
                sx={{ gridColumn: "span 1" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Género"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.genero.toLowerCase()}
                name="genero"
                error={!!touched.genero && !!errors.genero}
                helperText={touched.genero && errors.genero}
                sx={{ gridColumn: "span 1" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="date"
                label="Fecha de Nacimiento"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.fecha_nacimiento}
                name="fecha_nacimiento"
                error={!!touched.fecha_nacimiento && !!errors.fecha_nacimiento}
                helperText={touched.fecha_nacimiento && errors.fecha_nacimiento}
                sx={{ gridColumn: "span 1" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Teléfono"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.telefono}
                name="telefono"
                error={!!touched.telefono && !!errors.telefono}
                helperText={touched.telefono && errors.telefono}
                sx={{ gridColumn: "span 1" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Dirección"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.direccion}
                name="direccion"
                error={!!touched.direccion && !!errors.direccion}
                helperText={touched.direccion && errors.direccion}
                sx={{ gridColumn: "span 4" }}
              />
              {values.tipo_usuario === "paciente" && (
                <TextField
                  fullWidth
                  variant="filled"
                  type="text"
                  label="Resultado de Detección"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  value={values.resultado}
                  name="resultado"
                  error={!!touched.resultado && !!errors.resultado}
                  helperText={touched.resultado && errors.resultado}
                  sx={{ gridColumn: "span 4" }}
                />
              )}
            </Box>
            <Box display="flex" justifyContent="end" mt="20px">
              <Button type="submit" color="secondary" variant="contained">
                Modificar Usuario
              </Button>
            </Box>
          </form>
        )}
      </Formik>
    </Box>
  );
};

const phoneRegExp =
  /^((\+[1-9]{1,4}[ -]?)|(\([0-9]{2,3}\)[ -]?)|([0-9]{2,4})[ -]?)*?[0-9]{3,4}[ -]?[0-9]{3,4}$/;

const password =
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[.@$!%*?&])[A-Za-z\d.@$!%*?&]+$/;
const checkoutSchema = yup.object().shape({
  id: yup
    .number()
    .typeError("ID debe ser un número")
    .required("ID es requerida"),
  tipo_usuario: yup
    .string()
    .oneOf(["paciente", "doctor"], "Debe seleccionar 'paciente' o 'doctor'")
    .required("Campo obligatorio"),
  nombre: yup.string().required("required"),
  correo: yup.string().email("invalid email").required("required"),
  usuario: yup.string().required("required"),
  contraseña: yup
    .string()
    .required("La contraseña es requerida")
    .min(8, "La contraseña debe tener al menos 8 caracteres")
    .matches(
      password,
      "La contraseña debe contener al menos una letra minúscula, una letra mayúscula, un número y un carácter especial"
    ),
  imagen: yup.string().required("required"),
  edad: yup
    .number()
    .typeError("Edad debe ser un número")
    .required("Edad es requerida"),
  genero: yup
    .string()
    .oneOf(
      ["masculino", "femenino"],
      "Debe seleccionar 'masculino' o 'femenino'"
    )
    .required("Campo obligatorio"),
  fecha_nacimiento: yup
    .date()
    .required("La fecha de nacimiento es requerida")
    .max(
      new Date(),
      "La fecha de nacimiento no puede ser posterior a la fecha actual"
    ),
  telefono: yup
    .string()
    .matches(phoneRegExp, "Phone number is not valid")
    .required("required"),
  direccion: yup.string().required("required"),
  resultado: yup.string().required("required"),
});
const initialValues = {
  id: "",
  tipo_usuario: "",
  nombre: "",
  correo: "",
  usuario: "",
  contraseña: "",
  imagen: "",
  edad: "",
  genero: "",
  fecha_nacimiento: "",
  telefono: "",
  direccion: "",
  resultado: "",
};

export default Modificar;
