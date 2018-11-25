/* global getAssetRegistry getFactory emit */

/**
 * ReportConsumption transaction processor function.
 * @param {org.example.basic.ReportConsumption} tx The sample transaction instance.
 * @transaction
 */
async function ReportConsumption(tx) {  // eslint-disable-line no-unused-vars


  const bonusRegistry = await getAssetRegistry('org.example.basic.Bonus');

  const energyRegistry = await getAssetRegistry('org.example.basic.EnergyAmount');

  var allEnergy = await energyRegistry.getAll(); 

  var allEnergyFiltered = allEnergy.filter(energyObj => {
    return energyObj.consumer.getIdentifier() == tx.plug.plugId
  });
  var factory = getFactory();
  var energyamount = factory.newResource('org.example.basic', 'EnergyAmount', 'ENERGY_ITEM_' + Math.random());

  energyamount.value = tx.amount;
  energyamount.consumer = tx.plug;
  energyamount.position = "" + (allEnergyFiltered.length + 1);


  await energyRegistry.add(energyamount);


  }

/**
 * CreateBonus transaction processor function.
 * @param {org.example.basic.CreateBonus} tx The sample transaction instance.
 * @transaction
 */
async function CreateBonus(tx) {  // eslint-disable-line no-unused-vars


  const bonusRegistry = await getAssetRegistry('org.example.basic.Bonus');

  var allBonus = await bonusRegistry.getAll();

  var factory = getFactory();
  var newBonus = factory.newResource('org.example.basic', 'Bonus', 'BONUS_ITEM_' + Math.random());

  newBonus.generate = tx.generate;
  newBonus.euroCent = tx.euroCent;
  newBonus.position = "" + (allBonus.length + 1);

  await bonusRegistry.add(newBonus);


}

/**
 * UpdateBalance transaction processor function.
 * @param {org.example.basic.UpdateBalance} tx The sample transaction instance.
 * @transaction
 */
async function UpdateBalance(tx) { 


  const bonusRegistry = await getAssetRegistry('org.example.basic.Bonus');
  const energyRegistry = await getAssetRegistry('org.example.basic.EnergyAmount');
  const smartPlugRegistry = await getParticipantRegistry('org.example.basic.SmartPlug');

  const bonusList = await bonusRegistry.getAll();


  const energyList = await energyRegistry.getAll();


  var newestBonus = bonusList.filter(bonus => {
    return bonus.position == bonusList.length
  });

  var energyListFiltered = energyList.filter(energyObj => {
    return energyObj.consumer.getIdentifier() == tx.plug.plugId
  });

  var newestEnergyAmount = energyListFiltered.filter(energyObj => {
    return energyObj.position == energyListFiltered.length;
  });


  tx.plug.currentBalance = "" + (parseInt(tx.plug.currentBalance) + (newestBonus[0].euroCent * newestEnergyAmount[0].value));


  await smartPlugRegistry.update(tx.plug);


}


