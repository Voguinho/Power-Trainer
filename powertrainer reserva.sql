-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 20/10/2024 às 22:13
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `powertrainer`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `avaliacoes`
--

CREATE TABLE `avaliacoes` (
  `id` int(11) NOT NULL,
  `comentario` varchar(500) DEFAULT NULL,
  `avaliado_id` int(11) DEFAULT NULL,
  `personalidade` double DEFAULT NULL,
  `habilidade` double DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `grupo_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `calendario`
--

CREATE TABLE `calendario` (
  `id` int(11) NOT NULL,
  `parceiro` varchar(50) DEFAULT NULL,
  `comentario` varchar(100) DEFAULT NULL,
  `data_hora` datetime DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `esporte`
--

CREATE TABLE `esporte` (
  `id` int(11) NOT NULL,
  `nome` varchar(115) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `esporte`
--

INSERT INTO `esporte` (`id`, `nome`) VALUES
(1, 'Futebol'),
(2, 'Tênis de mesa ');

-- --------------------------------------------------------

--
-- Estrutura para tabela `favoritos`
--

CREATE TABLE `favoritos` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) DEFAULT NULL,
  `usuariofavorito_id` int(11) DEFAULT NULL,
  `data_criacao` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `grupo`
--

CREATE TABLE `grupo` (
  `id` int(11) NOT NULL,
  `nome` varchar(100) DEFAULT NULL,
  `horario` datetime DEFAULT NULL,
  `genero` varchar(100) DEFAULT NULL,
  `limite_membros` double DEFAULT NULL,
  `descricao` varchar(2000) DEFAULT NULL,
  `limite_pelada` double DEFAULT NULL,
  `esportes_id` int(11) DEFAULT NULL,
  `Local_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `grupo`
--

INSERT INTO `grupo` (`id`, `nome`, `horario`, `genero`, `limite_membros`, `descricao`, `limite_pelada`, `esportes_id`, `Local_id`) VALUES
(1, 'Fute dos cria', '2024-10-12 10:30:00', 'Masculino', 20, 'Fute para os cria jogar', 20, 1, 1),
(2, 'Tênis de mesa da galera ', '2024-10-12 10:30:00', 'Misto', 20, 'Grupo para quem gosta de TM', 20, 2, 1),
(5, 'Tênis de mesa masculino', '2024-10-12 10:30:00', 'Masculino', 20, 'Grupo para quem que virar profissional ', 20, 2, 1),
(6, 'Tênis de mesa feminino', '2024-10-12 10:30:00', 'Feminino', 20, 'Grupo para quem que virar profissional ', 20, 2, 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `local`
--

CREATE TABLE `local` (
  `id` int(11) NOT NULL,
  `nome` varchar(115) DEFAULT NULL,
  `CEP` double DEFAULT NULL,
  `cidade` varchar(100) DEFAULT NULL,
  `rua` varchar(20) DEFAULT NULL,
  `numero` double DEFAULT NULL,
  `bairro` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `local`
--

INSERT INTO `local` (`id`, `nome`, `CEP`, `cidade`, `rua`, `numero`, `bairro`) VALUES
(1, 'Quadra da igreja', 23423423432, 'Belo Horizonte', 'tads', 12, 'asdfadf'),
(2, 'Quadra da igreja', 23423423432, 'Belo Horizonte', 'tads', 12, 'asdfadf');

-- --------------------------------------------------------

--
-- Estrutura para tabela `mensagem`
--

CREATE TABLE `mensagem` (
  `id` int(11) NOT NULL,
  `mensagem` varchar(500) DEFAULT NULL,
  `tipo_msg` varchar(20) DEFAULT NULL,
  `midia` blob DEFAULT NULL,
  `data_criacao` datetime DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `grupo_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `mensagem`
--

INSERT INTO `mensagem` (`id`, `mensagem`, `tipo_msg`, `midia`, `data_criacao`, `usuario_id`, `grupo_id`) VALUES
(1, 'Oi galera', NULL, NULL, '2024-10-11 00:00:01', 1, 1),
(2, 'Tudo beleza?', NULL, NULL, '2024-10-11 00:00:02', 2, 1),
(3, 'Bora jogar um fute', NULL, NULL, '2024-10-11 00:00:03', 2, 1);

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `nome` varchar(50) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `senha` varchar(80) DEFAULT NULL,
  `imagem_perfil` blob DEFAULT NULL,
  `genero` varchar(10) DEFAULT NULL,
  `nivel_de_treino` varchar(10) DEFAULT NULL,
  `nota_geral` double DEFAULT NULL,
  `objetivo` varchar(100) DEFAULT NULL,
  `data_criacao` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuario`
--

INSERT INTO `usuario` (`id`, `nome`, `email`, `senha`, `imagem_perfil`, `genero`, `nivel_de_treino`, `nota_geral`, `objetivo`, `data_criacao`) VALUES
(1, 'Tiago Morel', 'tiagomo207@gmail.com', 'fatanuca', NULL, 'Masculino', 'Iniciante', 5, 'Treinar Pesado', '0000-00-00'),
(2, 'Beatriz', 'bia@gmail.com', 'fatanuca', NULL, 'Feminino', 'Iniciante', 2, 'Treinar', '0000-00-00');

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuario_grupo`
--

CREATE TABLE `usuario_grupo` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `grupo_id` int(11) DEFAULT NULL,
  `estrelas` double DEFAULT NULL,
  `confirmacao` varchar(3) DEFAULT NULL,
  `pago` varchar(3) DEFAULT NULL,
  `adm` varchar(3) DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `usuario_grupo`
--

INSERT INTO `usuario_grupo` (`id`, `usuario_id`, `grupo_id`, `estrelas`, `confirmacao`, `pago`, `adm`) VALUES
(4, 2, 1, 0, NULL, NULL, 'N'),
(5, 2, 2, 0, NULL, NULL, 'N'),
(6, 2, 5, 0, NULL, NULL, 'N'),
(7, 2, 6, 0, NULL, NULL, 'N'),
(8, 1, 2, 0, NULL, NULL, 'N'),
(9, 1, 1, 0, NULL, NULL, 'N'),
(10, 1, 2, 0, NULL, NULL, 'N'),
(11, 1, 2, 0, NULL, NULL, 'N');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `avaliacoes`
--
ALTER TABLE `avaliacoes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `grupo_id` (`grupo_id`),
  ADD KEY `avaliado` (`avaliado_id`);

--
-- Índices de tabela `calendario`
--
ALTER TABLE `calendario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Índices de tabela `esporte`
--
ALTER TABLE `esporte`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `favoritos`
--
ALTER TABLE `favoritos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuariofavorito_id` (`usuariofavorito_id`);

--
-- Índices de tabela `grupo`
--
ALTER TABLE `grupo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `esportes_id` (`esportes_id`),
  ADD KEY `Local_id` (`Local_id`);

--
-- Índices de tabela `local`
--
ALTER TABLE `local`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `mensagem`
--
ALTER TABLE `mensagem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `grupo_id` (`grupo_id`) USING BTREE;

--
-- Índices de tabela `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- Índices de tabela `usuario_grupo`
--
ALTER TABLE `usuario_grupo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `grupo_id` (`grupo_id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `avaliacoes`
--
ALTER TABLE `avaliacoes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `calendario`
--
ALTER TABLE `calendario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `esporte`
--
ALTER TABLE `esporte`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `favoritos`
--
ALTER TABLE `favoritos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `grupo`
--
ALTER TABLE `grupo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `local`
--
ALTER TABLE `local`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `mensagem`
--
ALTER TABLE `mensagem`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de tabela `usuario_grupo`
--
ALTER TABLE `usuario_grupo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `avaliacoes`
--
ALTER TABLE `avaliacoes`
  ADD CONSTRAINT `avaliacoes_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`),
  ADD CONSTRAINT `avaliacoes_ibfk_2` FOREIGN KEY (`grupo_id`) REFERENCES `grupo` (`id`),
  ADD CONSTRAINT `avaliado` FOREIGN KEY (`avaliado_id`) REFERENCES `usuario` (`id`);

--
-- Restrições para tabelas `calendario`
--
ALTER TABLE `calendario`
  ADD CONSTRAINT `calendario_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);

--
-- Restrições para tabelas `favoritos`
--
ALTER TABLE `favoritos`
  ADD CONSTRAINT `favoritos_ibfk_1` FOREIGN KEY (`usuariofavorito_id`) REFERENCES `usuario` (`id`);

--
-- Restrições para tabelas `grupo`
--
ALTER TABLE `grupo`
  ADD CONSTRAINT `grupo_ibfk_1` FOREIGN KEY (`esportes_id`) REFERENCES `esporte` (`id`),
  ADD CONSTRAINT `grupo_ibfk_2` FOREIGN KEY (`Local_id`) REFERENCES `local` (`id`);

--
-- Restrições para tabelas `mensagem`
--
ALTER TABLE `mensagem`
  ADD CONSTRAINT `mensagem_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`),
  ADD CONSTRAINT `mensagem_ibfk_2` FOREIGN KEY (`grupo_id`) REFERENCES `grupo` (`id`);

--
-- Restrições para tabelas `usuario_grupo`
--
ALTER TABLE `usuario_grupo`
  ADD CONSTRAINT `usuario_grupo_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`),
  ADD CONSTRAINT `usuario_grupo_ibfk_2` FOREIGN KEY (`grupo_id`) REFERENCES `grupo` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
