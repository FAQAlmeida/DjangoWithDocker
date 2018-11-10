my_username = "FreqAbsoluto";
git_hub_path = "https://api.github.com";
repos_path = "/users/{user}/repos";
readme_path = "/repos/{owner}/{repo}/readme";
request = new XMLHttpRequest();

function show_repositories() {
    let path = git_hub_path + repos_path.replace("{user}", my_username);
    request.onreadystatechange = function(){
      if(this.readyState === 4 && this.status === 200){
          try {
              const reposJSON = JSON.parse(this.responseText);
              document.getElementById("collapse_repo_x").innerHTML = mount_repos_html(reposJSON);
          }catch (e) {
              document.getElementById("collapse_repo_x").innerText = "Error: {0}".format(e.toString());
          }
          // saveText(JSON.stringify(reposJSON), "reposJson.json");
          console.log(this.responseText);
      }
    };
    request.open("GET", path, true);
    request.send();
}
function show_readme(repository, id) {
    let path = git_hub_path + readme_path.replace("{owner}", my_username).replace("{repo}", repository);
    request.onreadystatechange = function(){
        if(this.readyState === 4 && this.status === 200){
            try {
                const readmeJSON = JSON.parse(this.responseText);
                document.getElementById(id).innerHTML = readmeJSON.content;
            }catch (e) {
                document.getElementById(id).innerText = "Error: {0}".format(e.toString());
            }
            // saveText(JSON.stringify(readmeJSON), "readmeJSON.json");
            console.log(this.responseText);
        }
    };
    request.open("GET", path, true);
    request.send();
}
String.prototype.format = function () {
    let a = this;
    for (let k in arguments) {
        a = a.replace(new RegExp("\\{" + k + "\\}", 'g'), arguments[k]);
    }
    return a;
};

function mount_repos_html(repos_github_json) {
    let html_response = "";
    for (let i = 0; i < repos_github_json.length; i++) {
        let repositorio = repos_github_json[i].name;
        let html_url = repos_github_json[i].html_url;
        let description = repos_github_json[i].description;
        let language = repos_github_json[i].language;
        let id = repositorio + i;
        let row_pat =  
            "<div class='row my_row'>"+
                "{0}"+
            "</div>";
        let pattern =
            "<div class='panel-group'>" +
                "<div class='panel panel-default'>" +
                    "<div class='panel-heading'>" +
                        "<h4 class='panel-title' id='title-panel'>" +
                            "<a data-toggle='collapse' href='#{0}'>{1}</a>" +
                        "</h4>" +
                        "<h6 id='language'>Linguagem: {4}</h6>" +
                    "</div>" +
                    "<div id='{0}' class='panel-collapse collapse'>" +
                        "<div class='panel-body' onmouseover='show_readme({1}, {0})'>{2}</div>" +
                        "<div class='panel-footer'><a href='{3}' target='_blank' title='{1}'>GitHub link: {1}</a></div>" +
                    "</div>" +
                "</div>" +
            "</div>";
        pattern = pattern.format(id, repositorio, description, html_url, language);
        pattern = (i % 3 == 0) ? row_pat.format(pattern) : pattern;
        html_response += pattern;
    }
    return html_response;
}