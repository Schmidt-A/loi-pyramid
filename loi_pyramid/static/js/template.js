function renderTemplate(parent, id, markup) {
	if (parent && parent.children.length > 0) {
		parent.removeChild(parent.children[0]);
	}

	history.pushState(null, '', `/${id}`)

	let container = document.createElement("div");
	container.id = id;
    container.innerHTML = markup;

    parent.appendChild(container);
}

const router = {
	'/app/': loginPage,
	'/app/login': loginPage,
	'/app/account': accountCharacterPage,
	'/app/characters': charactersPage
}