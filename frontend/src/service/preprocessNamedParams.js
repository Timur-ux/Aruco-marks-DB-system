import { getSHA256Hash } from "boring-webcrypto-sha256";


const preprocessNamedParams = async ({ params, fields }) => {
  const paramLen = Object.keys(params).length;
  if (paramLen != fields.length) {
    console.error(
      "preprocessNamedParams: params and fields has different length",
      "\nParams: ",
      params,
      "\nFields: ",
      fields,
    );
    return {};
  }

  for (let i = 0; i < paramLen; i++) {
    if (fields[i].type == "int") {
      params[fields[i].name] = Number(params[fields[i].name]);
      console.log("preprocessNamedParams: int");
    } else if (fields[i].type == "parameters_dict") {
      params[fields[i].name] = JSON.parse(params[fields[i].name]);
      console.log("preprocessNamedParams: parameters_dict");
    } else if (fields[i].type == "string") {
      console.log("preprocessNamedParams: string");
    } else if (fields[i].type == "string(sha256)") {
      params[fields[i].name] = await getSHA256Hash(params[fields[i].name]);
      console.log("preprocessNamedParams: string(sha256)");
    } else {
      console.warn(
        "preprocessNamedParams: undefined field type: ",
        fields[i].type,
      );
    }
  }

  console.log("preprocessNamedParams: result: ", params);
  return params;
};

export default preprocessNamedParams;
