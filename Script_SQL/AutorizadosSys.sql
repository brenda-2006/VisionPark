CREATE DATABASE UsuariosAutorizados;	-- Creación de la base de datos de los directivos autorizados para ingresar al sistema.
GO										-- Ejecutar todo lo anterior antes de continuar.
USE UsuariosAutorizados;				-- Todo lo que se haga será dentro de la base de datos creada.

CREATE TABLE Autorizados (
	Id INT PRIMARY KEY IDENTITY(1,1),
	Usuario NVARCHAR(50) UNIQUE NOT NULL,
	Contraseña NVARCHAR(255) UNIQUE NOT NULL,
	Nombre_Completo NVARCHAR(100) UNIQUE NOT NULL,
	Documento_Identificación NVARCHAR(30) UNIQUE NOT NULL,
	Edad INT,
	Celular NVARCHAR(10) NOT NULL,
	Direccion NVARCHAR(40) NOT NULL,
	Rol NVARCHAR(50) NOT NULL,
	UltimoIni_Sesion DATETIME
);

INSERT INTO Autorizados (
    Usuario,
    Contraseña,
    Nombre_Completo,
    Documento_Identificación,
    Edad,
    Celular,
    Direccion,
    Rol,
    UltimoIni_Sesion
)
VALUES (
    'admin',
    '1234',  
    'Brenda Pérez',
    '100200300',
    28,
    '3012345678',
    'Torre A, Apto 302',
    'Administrador',
    NULL
);