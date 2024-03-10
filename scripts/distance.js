//stolen from the internet
function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) //returns distance in km and angle in degrees
{
    var R = 6371; // Radius of the earth in km
    var dLat = degreesToRadians(lat2-lat1);  // degreesToRadians below
    var dLon = degreesToRadians(lon2-lon1); 
    var a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(degreesToRadians(lat1)) * Math.cos(degreesToRadians(lat2)) * 
      Math.sin(dLon/2) * Math.sin(dLon/2)
      ; 
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    var d = R * c; // Distance in km
    

    const y = Math.sin(dLon) * Math.cos(degreesToRadians(lat2));
    const x = Math.cos(degreesToRadians(lat1)) * Math.sin(degreesToRadians(lat2)) -
              Math.sin(degreesToRadians(lat1)) * Math.cos(degreesToRadians(lat2)) * Math.cos(dLon);
    const angleRadians = Math.atan2(y, x);
    const angleDegrees = (angleRadians * 180 / Math.PI + 360) % 360; // got from chatGPT lmao

    return [d, angleDegrees];
}
  
function degreesToRadians(degrees) {
    return degrees * Math.PI / 180;
}

function radiansToDegrees(radians) {
    return radians * 180 / Math.PI;
}

function calculateNewCoordinates(latitude, longitude, bearing, distance) {
    const earthRadiusKm = 6371;
    const angularDistance = distance / earthRadiusKm; // Convert distance to angular distance

    const lat1 = degreesToRadians(latitude);
    const lon1 = degreesToRadians(longitude);
    const bearingRadians = degreesToRadians(bearing);

    const lat2 = Math.asin(Math.sin(lat1) * Math.cos(angularDistance) +
                           Math.cos(lat1) * Math.sin(angularDistance) * Math.cos(bearingRadians));
    const lon2 = lon1 + Math.atan2(Math.sin(bearingRadians) * Math.sin(angularDistance) * Math.cos(lat1),
                                   Math.cos(angularDistance) - Math.sin(lat1) * Math.sin(lat2));

    return {
        latitude: radiansToDegrees(lat2),
        longitude: radiansToDegrees(lon2)
    };
}

function timeToHitGround(velocity, height)
{
    const discriminant = Math.sqrt(Math.pow(velocity, 2) + 2 * g * height);
    const time = (-velocity + discriminant) / g;

    return time;

}
var globalDataQueue = []
var yVelocity = 0
var maxLength = 3
const gravity = -9.81

function newPointAdded(newPoint) // expecting an object form of the new row
{
    // add data into queue and remove old element if bigger than maxLength
    globalDataQueue.push(newPoint)
    if (globalDataQueue.length() > maxLength)
    {
        globalDataQueue.shift()
    }

    //get y velocity
    let oldestPoint = globalDataQueue[0]
    let lastPoint = globalDataQueue[maxLength-2]
    if (lastPoint.Altitude < newPoint.Altutude) //if we still rising, we don't really care to make prediction
    {
        console.log('Still rising!')
        return false
    }
    yVelocity += gravity*(newPoint[updated_at] - lastPoint[updated_at])
    let timeRemaining = timeToHitGround(yVelocity, newPoint.Altitude)
    console.log("Time to hit the ground (s):", timeRemaining);

    //get x velocity
    let temp = getDistanceFromLatLonInKm(oldestPoint.Latitude, oldestPoint.Longitude, newPoint.Latitude, newPoint.Longitude)
    let distanceBetweenPoints = temp[0]
    let angleBetweenPoints = temp[1]

    let speed = distanceBetweenPoints/(newPoint[updated_at] - oldestPoint[updated_at])

    //predicted distance to travel
    let travelDistance = speed*timeRemaining

    //predicted coordinates
    let newCoords = calculateNewCoordinates(newPoint.Latitude, newPoint.Longitude, angleBetweenPoints, travelDistance)
    console.log("New Latitude: ", newCoords.latitude)
    console.log("New Longitude: ", newCoords.longitude)

    return true
}