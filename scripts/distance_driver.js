let global_data_index = 65

function addNewPoint()
{
    let newPoint = global_data[global_data_index]
    newPointAdded(newPoint)
    global_data_index += 1
}