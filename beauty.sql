/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2018/7/3 20:29:50                            */
/*==============================================================*/


drop table if exists address;

drop table if exists admin;

drop table if exists cart;

drop table if exists g_category;

drop table if exists g_category2;

drop table if exists goods;

drop table if exists goodsorder;

drop table if exists orders;

drop table if exists user;

/*==============================================================*/
/* Table: address                                               */
/*==============================================================*/
create table address
(
   id                   int not null auto_increment,
   use_id               int,
   u_tel                varchar(11) not null,
   u_provinces          varchar(1024) not null,
   u_city               varchar(1024) not null,
   u_county             varchar(1024) not null,
   u_street             varchar(1024) not null,
   u_email              varchar(1024) not null,
   u_detailaddr         varchar(4096) not null,
   u_addrstatus         int not null,
   primary key (id)
);

/*==============================================================*/
/* Table: admin                                                 */
/*==============================================================*/
create table admin
(
   id                   int not null auto_increment,
   a_account            varchar(50) not null,
   a_pwd                varchar(128) not null,
   primary key (id)
);

/*==============================================================*/
/* Table: cart                                                  */
/*==============================================================*/
create table cart
(
   id                   int not null auto_increment,
   u_id                 int not null,
   g_id                 int not null,
   g_num                int not null,
   is_select            bool not null default 1,
   primary key (id)
);

/*==============================================================*/
/* Table: g_category                                            */
/*==============================================================*/
create table g_category
(
   id                   int not null,
   c_name               varchar(50),
   c_code               int,
   c_desc               varchar(255),
   primary key (id)
);

alter table g_category comment '商品一级分类';

/*==============================================================*/
/* Table: g_category2                                           */
/*==============================================================*/
create table g_category2
(
   id                   int not null,
   c2_name              varchar(50),
   c2_desc              varchar(255),
   c2_code              int,
   c_code               int not null,
   primary key (id)
);

alter table g_category2 comment '商品二级分类';

/*==============================================================*/
/* Table: goods                                                 */
/*==============================================================*/
create table goods
(
   id                   int not null auto_increment,
   c_code               int not null,
   c2_code              int not null,
   g_name               varchar(50) not null,
   g_desc               varchar(255),
   g_info               varchar(255),
   g_mktprice           float not null,
   g_price              float not null,
   g_goodsprops         varchar(255),
   g_pics               varchar(255),
   g_inventory          int not null default 99,
   g_sale               int not null default 0,
   g_status             bool not null default 0,
   g_createtime         datetime not null default CURRENT_TIMESTAMP,
   g_changetime         datetime not null,
   g_class              varchar(255) not null,
   primary key (id)
);

alter table goods comment '商品详情表';

/*==============================================================*/
/* Table: goodsorder                                            */
/*==============================================================*/
create table goodsorder
(
   id                   int not null auto_increment,
   ord_id               int not null,
   g_id                 int not null,
   primary key (id)
);

/*==============================================================*/
/* Table: orders                                                */
/*==============================================================*/
create table orders
(
   id                   int not null auto_increment,
   u_id                 int not null,
   o_price              float not null,
   o_status             int not null default 0,
   o_creattime          datetime,
   o_changetime         datetime,
   o_num                int not null,
   o_reciveaddr         varchar(512) not null,
   primary key (id)
);

/*==============================================================*/
/* Table: user                                                  */
/*==============================================================*/
create table user
(
   id                   int not null auto_increment,
   u_name               varchar(1024) not null,
   u_pwd                varchar(1024) not null,
   u_ticket             longtext not null,
   u_outtime            datetime not null,
   primary key (id)
);

alter table address add constraint FK_Relationship_1 foreign key (use_id)
      references user (id) on delete restrict on update restrict;

alter table cart add constraint FK_Relationship_4 foreign key (u_id)
      references user (id) on delete restrict on update restrict;

alter table cart add constraint FK_Relationship_5 foreign key (g_id)
      references goods (id) on delete restrict on update restrict;

alter table g_category2 add constraint FK_Relationship_3 foreign key (c_code)
      references g_category (id) on delete restrict on update restrict;

alter table goodsorder add constraint FK_Relationship_7 foreign key (g_id)
      references goods (id) on delete restrict on update restrict;

alter table goodsorder add constraint FK_Relationship_8 foreign key (ord_id)
      references orders (id) on delete restrict on update restrict;

alter table orders add constraint FK_Relationship_9 foreign key (u_id)
      references user (id) on delete restrict on update restrict;

