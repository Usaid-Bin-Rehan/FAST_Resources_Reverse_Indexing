const getElementById = (id) => {
  return document.getElementById(id);
};

const getElementBySelector = (selector) => {
  return document.querySelector(selector);
};

const TABLE_ELEMENT = getElementById("links");
const LOADER_ELEMENT = getElementById("loader");
const SEARCH_INPUT_ELEMENT = document.querySelector("#search_input input");
const SEARCH_BUTTON_ELEMENT = document.getElementById("submit_button");
const QUERY_STRING_EMPTY_MESSAGE = "Query string is empty! 😭";
const NO_RESOURCES_FOUND_MESSAGE = "No resources found! ❌";

const getQueryString = () => {
  return SEARCH_INPUT_ELEMENT.value;
};

const hideElement = (element) => {
  element.style.display = "none";
};

const removeAllChildren = (element) => {
  element.innerHTML = "";
};

const createLinkTableRow = (link) => {
  const tableRow = document.createElement("tr");
  const tableDescriptor = document.createElement("td");
  const anchorTag = document.createElement("a");
  anchorTag.href = link;
  anchorTag.innerText = link;
  tableDescriptor.appendChild(anchorTag);
  tableRow.appendChild(tableDescriptor);

  return tableRow;
};

const addTableRows = (data) => {
  const tableBody = document.querySelector("#links tbody");

  data.forEach((element) => {
    const linkTableRow = createLinkTableRow(element);
    tableBody.appendChild(linkTableRow);
  });

  hideElement(LOADER_ELEMENT);
  TABLE_ELEMENT.style.display = "block";
  SEARCH_INPUT_ELEMENT.value = "";
};

const searchForResources = () => {
  const searchQuery = getQueryString();
  if (searchQuery) {
    const tableBody = document.querySelector("#links tbody");
    hideElement(TABLE_ELEMENT);
    removeAllChildren(tableBody);
    LOADER_ELEMENT.style.display = "flex";

    const URL = `https://pgym2y6r7g.execute-api.eu-west-1.amazonaws.com/default/FAST-Resources_Reverse-Index?query=${searchQuery}`;
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-API-KEY": "vVl351vGfo55rA1dY68F21TR8Nj1nBJw2wXcfFBi",
      },
    };
    fetch(URL, options)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data.length) {
          addTableRows(data);
        } else {
          M.toast({ html: NO_RESOURCES_FOUND_MESSAGE });
        }
        hideElement(LOADER_ELEMENT);
      });
  } else {
    M.toast({ html: QUERY_STRING_EMPTY_MESSAGE });
  }

};

SEARCH_BUTTON_ELEMENT.addEventListener("click", searchForResources);
