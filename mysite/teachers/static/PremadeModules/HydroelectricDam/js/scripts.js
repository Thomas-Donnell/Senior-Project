function calculatePE() {
    const mass = document.getElementById('mass').value;
    const height = document.getElementById('height').value;
    const g = 9.81; 
    
    const PE = mass * g * height;
    
    document.getElementById('result').textContent = PE.toFixed(2);
}

function calculateForce() {
    const mass = document.getElementById('mass1').value;
    const g = 9.81; 
    
    const force = mass * g;
    
    document.getElementById('result1').textContent = force.toFixed(2);
}

function calculateWork() {
    const force = document.getElementById('force').value;
    const distance = document.getElementById('distance').value;
    
    const work = force * distance;
    
    document.getElementById('result2').textContent = work.toFixed(2);
}

function calculatePower() {
    const work = document.getElementById('work').value;
    const time = document.getElementById('time').value;
    
    const power = work / time;
    
    document.getElementById('result3').textContent = power.toFixed(2);
}

function calculatePEPVC() {
    const mass = document.getElementById('massPVC').value;
    const height = document.getElementById('heightPVC').value;
    const conversion = 39.37;
    const conversionCalc = height / conversion;
    const g = 9.81; 
    
    const PE = mass * g * conversionCalc;
    
    document.getElementById('result4').textContent = PE.toFixed(2);
}

function calculateWater(){
    const gallons = document.getElementById('gallons').value;
    const gallTokg = 3.79;

    const result = gallons * gallTokg;

    document.getElementById('result5').textContent = result.toFixed(2);
    document.getElementById('massPP').textContent = result.toFixed(2);
}

function calculatePP() {
    const mass = document.getElementById('massPP').textContent;
    const height = document.getElementById('heightPP').textContent;

    if(isNaN(mass) || isNaN(height)) {
        console.error("Mass and height must be valid numbers");
        return; // Stop the function if either value is not a valid number
    }

    const PE = mass * 9.81 * height;
    console.log(PE);
    document.getElementById('PEPP').textContent = PE.toFixed(2);

    const result = PE * 0.9;
    console.log(result);

    document.getElementById('result6').textContent = result.toFixed(2);
}


function setPVCHeight(){
    const height = document.getElementById('heightSetPVC').value;
    document.getElementById('heightPP').textContent = height;
}

function calculateStudForce() {
    const mass = document.getElementById('studMass').value;
    const g = 9.81; 
    
    const force = mass * g;
    
    document.getElementById('studForceResult').textContent = force.toFixed(2);
    document.getElementById('studForceResult1').textContent = force.toFixed(2);
}

function calculateStudWork() {
    const mass = document.getElementById('studForceResult1').textContent;
    const distance = document.getElementById('studDist').value;
    
    const work = mass * distance;
    
    document.getElementById('studWorkResult').textContent = work.toFixed(2);
    document.getElementById('studWorkResult1').textContent = work.toFixed(2);
}

function calculateStudPower() {
    const work = document.getElementById('studWorkResult1').textContent;
    const time = document.getElementById('studTime').value;
    
    const power = work / time;
    
    document.getElementById('studPowerResult').textContent = power.toFixed(2);
}

function calculateStudEfficiency(){
    const watts = document.getElementById('studWatts').value;
    const ratio = 0.9;

    const effResult = watts * ratio;

    document.getElementById('studEfficiencyResult').textContent = effResult.toFixed(2);

    if(effResult < 10){
        document.getElementById('diodeResult').textContent = "Diode does not light up.";

    } else if(effResult >= 10 && effResult<=12){
        document.getElementById('diodeResult').textContent = "Diode succesfully lights up.";
    } else{
        document.getElementById('diodeResult').textContent = "Diode Explodes or Cracks.";
    }
}