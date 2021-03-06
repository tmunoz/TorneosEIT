'use strict';

module.exports = (sequelize, DataTypes) => {
  let contestant = sequelize.define('contestant', {
    rut: {
      type: DataTypes.BIGINT,
      allowNull: false,
      primaryKey: true
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false
    },
    power: {
      type: DataTypes.BOOLEAN,
      allowNull: false
    }
  });

  contestant.associate = (models) => {
    contestant.belongsToMany(models.team, {
      through: 'contestant_teams',
      as: 'teams',
    });
  };
  return contestant;
};
