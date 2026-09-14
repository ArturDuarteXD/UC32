CREATE TABLE `clientes` (
  `id` integer PRIMARY KEY,
  `nome` varchar(255),
  `email` varchar(255) UNIQUE,
  `telefone` varchar(255),
  `data_cadastro` date
);

CREATE TABLE `produtos` (
  `id` integer PRIMARY KEY,
  `nome` varchar(255),
  `descricao` varchar(255),
  `preco` decimal,
  `estoque` integer
);

CREATE TABLE `pedidos` (
  `id` integer PRIMARY KEY,
  `cliente_id` integer,
  `data_pedido` date,
  `status` varchar(255)
);

CREATE TABLE `itens_pedido` (
  `id` integer PRIMARY KEY,
  `pedido_id` integer,
  `produto_id` integer,
  `quantidade` integer,
  `preco_unitario` decimal
);

ALTER TABLE `pedidos` ADD FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`);

ALTER TABLE `itens_pedido` ADD FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`);

ALTER TABLE `itens_pedido` ADD FOREIGN KEY (`produto_id`) REFERENCES `produtos` (`id`);
