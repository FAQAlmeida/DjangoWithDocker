my_username = "FreqAbsoluto";
git_hub_path = "https://api.github.com";
repos_path = "/users/{user}/repos";
readme_path = "/repos/{owner}/{repo}/readme";
request = new XMLHttpRequest();

function show_repositories() {
    let path = git_hub_path + repos_path.replace("{user}", my_username);
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            try {
                const reposJSON = JSON.parse(this.responseText);
                document.getElementById("repos").innerHTML = mount_repos_html(reposJSON);
            } catch (e) {
                console.error(e);
            }
            // saveText(JSON.stringify(reposJSON), "reposJson.json");
        } else if (this.readyState === 4 && (this.status === 404 || this.status === 403)) {
            console.log("Status da requisição: " + this.status + "\nMenssagem: " + this.responseText);
        } else if (this.readyState === 4) {
            console.log("Status da requisição: " + this.status + "\nMenssagem: " + this.responseText);
        }
    };
    request.open("GET", path, true);
    request.send();
}

/*
function show_readme(repository, id) {
    let path = git_hub_path + readme_path.replace("{owner}", my_username).replace("{repo}", repository);
    console.log(path);
    request.onreadystatechange = function(){
        if(this.readyState === 4 && this.status === 200){
            try {
                const readmeJSON = JSON.parse(this.responseText);
                document.getElementById(id).innerHTML = readmeJSON.content;
            }catch (e) {
                console.error(e);                
            }
            // saveText(JSON.stringify(readmeJSON), "readmeJSON.json");
            console.log(this.responseText);
        }else if(this.readyState === 4 && this.status === 404){
            try{
                  const msg = "O repositório não tem Readme.md file";

            }catch(e){
                console.error(e);
            }
        }
    };
    request.open("GET", path, true);
    request.send();
}*/

String.prototype.format = function () {
    let a = this;
    for (let k in arguments) {
        a = a.replace(new RegExp("\\{" + k + "\\}", 'g'), arguments[k]);
    }
    return a;
};

function random_emoji() {
    emojis = [
        '\u{2708}',
        '\u{23F0}',
        '\u{2693}',
        '\u{1F424}',
        '\u{1F388}',
        '\u{1F493}',
        '\u{1F3C6}',
        '\u{1F349}',
        '\u{1F389}',
        '\u{1F377}',
        '\u{1F3AA}',
        '\u{1F989}',
        '\u{1F9DB}',
        '\u{1F4FA}',
        '\u{1F3B1}',
        '\u{1F437}',
        '\u{1F1E7}',
        '\u{1F639}',
        '\u{1F436}',
        '\u{1F42B}',
        '\u{1F5FC}',
        '\u{1F494}',
        '\u{1F6E5}',
    ];
    let num = Math.floor(Math.random() * emojis.length);
    return emojis[num];
}

function mount_repos_html(repos_github_json) {
    let html_response = "<div class='row my_row'>";

    let cols = (window.innerWidth > 1000) ? 3 : 1;
    let width = Math.floor(100 / cols) - 2;
    for (let i = 0; i < repos_github_json.length; i++) {
        let repositorio = repos_github_json[i].name;
        let html_url = repos_github_json[i].html_url;
        let description = repos_github_json[i].description;
        let language = repos_github_json[i].language;
        let id = (repositorio.replace(new RegExp('[\.]', 'g'), '_')) + i;
        let creation = new Date(repos_github_json[i].created_at).toLocaleDateString();
        /*
            1: id -: Formado no processo
            2: repositorio -: Nome do repositório
            3: github link -: Link para o repositório no GitHub
            4: Language -: Linguagem usada no Projeto
            5: Creation -: Data da criação do repositório
        */
        let row_pat =
            "{0}" +
            "</div>" +
            "<div class='row my_row'>";
        let pattern =
            "<div class='column my_column' style='width:{6}%'>" +
            "<div class='panel-group my_panel_group'>" +
            "<div class='panel panel-default my_panel'>" +
            "<div class='panel-heading'>" +
            "<span class='emoji'>" + random_emoji() + "</span>" +
            "<h4 class='panel-title'>" +
            "<a data-toggle='collapse' class='my_repository' href='#{0}'>{1}</a>" +
            "</h4>" +
            "<h6 class='language'>Linguagem: {4}</h6>" +
            "</div>" +
            "<div id='{0}' class='panel-collapse collapse'>" +
            "<div id='{0}desc' class='panel-body my_description'><p>{2}</p>" +
            "</div>" +
            "<div class='panel-footer my_footer'>" +
            "<p class='creation'>Criado em: {5}</p>" +
            "<a class='github' href='{3}' target='_blank' title='{1}'>GitHub: {1}</a>" +
            "</div>" +
            "</div>" +
            "</div>" +
            "</div>" +
            "</div>";
        pattern = pattern.format(id, repositorio, description, html_url, language, creation, width);
        pattern = ((i + 1) % cols == 0 && i != 0) ? row_pat.format(pattern) : pattern;
        html_response += pattern;
    }
    return html_response;
}