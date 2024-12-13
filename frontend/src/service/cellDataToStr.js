const cellDataToStr = data => {
  if(data.constructor == Object)
    return data.id;
  return data.toString();
}

export default cellDataToStr;
