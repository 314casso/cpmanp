<template>
  <b-container class="bv-example-row">    
    <b-row class="justify-content-md-center">           
    <b-col col lg="6">
    <b-card title="Авторизация">    
    <b-form @submit="onSubmit" class="text-center">
      <b-form-group id="usernameGroup"                    
                    label-for="usernameInput">
        <b-form-input id="usernameInput"
                      type="text"
                      v-model="data.body.username"
                      required
                      placeholder="Имя пользователя">
        </b-form-input>
      </b-form-group>
      <b-form-group id="passwordGroup"                    
                    label-for="passwordInput">
        <b-form-input id="passwordInput"
                      type="password"
                      v-model="data.body.password"
                      required
                      placeholder="Пароль">
        </b-form-input>
      </b-form-group>            
      <b-alert show v-show="error" variant="danger">
        {{ error }}
      </b-alert>
      <b-button type="submit" variant="primary">Войти</b-button>            
    </b-form>
    </b-card>
    </b-col>    
    </b-row>
    <b-row>               
    </b-row>
  </b-container>
</template>

<script>
export default {
  data () {
    return {
      context: 'login context',
      data: {
        body: {
          username: 'admin',
          password: 'secret'
        },
        rememberMe: true
      },
      error: null
    }
  },
  mounted () {
    console.log(this.$auth.redirect())
    // Can set query parameter here for auth redirect or just do it silently in login redirect.
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      var redirect = this.$auth.redirect()
      this.$auth
        .login({
          data: this.data.body, // Axios
          rememberMe: this.data.rememberMe,
          redirect: { name: redirect ? redirect.from.name : 'Table' }
        })
        .then(
          () => {
            console.log('success ' + this.context)
          },
          res => {
            console.log('error ' + this.context)
            console.error(res.response)
            this.error = res.response.data.msg
          }
        )
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>