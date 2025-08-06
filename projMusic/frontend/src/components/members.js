

getUsersInRoom(){
        const requestOptions = {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                code: this.roomCode
            }),
        }

        fetch('/api/users-in-room', requestOptions)
            .then((response) => {
                if(response.ok){
                    return response.json()
                }else{
                    return {}
                }

            })
            .then((data) => {
                this.setState({
                    members: data
                })
            }) .catch((error) => {
                console.log("Request was unsuccessful: ", error)
        })
    }

    renderUsersInRoom(){
        const items = []
        for (let i = 0; i < this.members.length; i++) {
            items.push(
                <li value={this.members[i]} key={i}>User {this.members[i]}</li>
            );
        }
        return pass
    }