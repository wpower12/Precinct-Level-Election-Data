// Application Navigation JavaScript Document

function RefreshPage() {
	location.href = location.href;
	return true;
}

function GoTo(Page) {
	location.href = Page;
	return true;
}

function GoHome() {
	location.href = '/info/index.csp';
	return true;
}

function LogOutUpdate() {
	location.href = "/info/Close.csp";
	return true;
}

function ExitApp(Where) {
	location.href = Where;
	return true;
}

function NewLookup(LookupPage) {
	if (LookupPage=='') {
		LookupPage="Lookup.csp"
	}
	location.href = LookupPage;
	return true;
}

function BackToList() {
	location.href = "List.csp";
	return true;
}