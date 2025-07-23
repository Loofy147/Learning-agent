# Ansible

## Introduction

Ansible is an open-source software provisioning, configuration management, and application-deployment tool enabling infrastructure as code.

## Questions

<details>
<summary>Describe each of the following components in Ansible, including the relationship between them: * Task * Inventory * Module * Play * Playbook * Role </summary>
<br>
<b> Task – a call to a specific Ansible module Module – the actual unit of code executed by Ansible on your own host or a remote host. Modules are indexed by category (database, file, network, …) and also referred to as task plugins. Inventory – An inventory file defines hosts and/or groups of hosts on which Ansible tasks executed upon. The inventory file can be in one of many formats, depending on the inventory plugins you have. The most common formats are INI and YAML. Play – One or more tasks executed on a given host(s) Playbook – One or more plays. Each play can be executed on the same or different hosts Role – Ansible roles allows you to group resources based on certain functionality/service such that they can be easily reused. In a role, you have directories for variables, defaults, files, templates,handlers, tasks, and metadata. You can then use the role by simply specifying it in your playbook. </b>
</details>

<details>
<summary>How Ansible is different from other automation tools? (e.g. Chef, Puppet, etc.)</summary>
<br>
<b> Ansible is: * Agentless * Minimal run requirements (Python & SSH) and simple to use * Default mode is "push" (it supports also pull) * Focus on simpleness and ease-of-use </b>
</details>

<details>
<summary>True or False? Ansible follows the mutable infrastructure paradigm</summary>
<br>
<b> True. In immutable infrastructure approach, you'll replace infrastructure instead of modifying it.<br> Ansible rather follows the mutable infrastructure paradigm where it allows you to change the configuration of different components, but this approach is not perfect and has its own disadvantages like "configuration drift" where different components may reach different state for different reasons. </b>
</details>

<details>
<summary>True or False? Ansible uses declarative styleto describe the expected end state</summary>
<br>
<b> False. It uses a procedural style. </b>
</details>

<details>
<summary>What kind of automation you wouldn't do with Ansible and why?</summary>
<br>
<b> While it's possible to provision resources with Ansible, some prefer to use tools that follow immutable infrastructure paradigm. Ansible doesn't saves state by default. So a task that creates 5 instances for example, when executed again will create additional 5 instances (unless additional check is implemented or explicit names are provided) while other tools might check if 5 instances exist. If only 4 exist (by checking the state file for example), one additional instance will be created to reach the end goal of 5 instances. </b>
</details>

<details>
<summary>How do you list all modules and how can you see details on a specific module?</summary>
<br>
<br>
<b> 1. Ansible online docs 2. `ansible-doc -l` for list of modules and `ansible-doc [module_name]` for detailed information on a specificmodule </b>
</details>

<details>
<summary>What is an inventory file and how do you define one?</summary>
<br>
<b> An inventory file defines hosts and/or groups of hosts on which Ansible tasks executed upon. An example of inventory file:
<pre>
192.168.1.2
192.168.1.3
192.168.1.4

[web_servers]
190.40.2.20
190.40.2.21
190.40.2.22
</pre>
</b>
</details>

<details>
<summary>What is a dynamic inventory file? When you would use one?</summary>
<br>
<br>
<b> A dynamic inventory file tracks hosts from one or more sources like cloud providers and CMDB systems. You should use one when using external sources and especially when the hosts in your environment are being automatically<br> spun up and shut down, without you tracking every change in these sources. </b>
</details>

<details>
<summary>Modify the following task to use a variable instead of the value "zlib" and have "zlib" as the default in case the variable is not defined
<pre>
- name: Install a package
  package:
    name: "zlib"
    state: present
</pre>
</summary>
<br>
<b>
<pre>
- name: Install a package
  package:
    name: "{{ package_name|default('zlib') }}"
    state: present
</pre>
</b>
</details>

<details>
<summary>How to make the variable "use_var" optional?
<pre>
- name: Install a package
  package:
    name: "zlib"
    state: present
  use: "{{ use_var }}"
</pre>
</summary>
<br>
<b> With "default(omit)"
<pre>
- name: Install a package
  package:
    name: "zlib"
    state: present
  use: "{{ use_var|default(omit) }}"
</pre>
</b>
</details>

<details>
<summary>What would be the result of the following play?</summary>
<br>
<b>
<pre>
---
- name: Print information about my host
  hosts: localhost
  gather_facts: 'no'

  tasks:
    - name: Print hostname
      debug:
        msg: "It's me, {{ ansible_hostname }}"
</pre>
When given a written code, always inspect it thoroughly. If your answeris “this will fail” then you are right. We are using a fact (ansible_hostname), which is a gathered piece of information from the host we are running on. But in this case, we disabled facts gathering (gather_facts: no) so the variable would be undefined which will result in failure. </b>
</details>

<details>
<summary>When the value '2017'' will be used in this case: `{{ lookup('env', 'BEST_YEAR') | default('2017', true) }}`?</summary>
<br>
<b> when the environment variable 'BEST_YEAR' is empty or false. </b>
</details>

<details>
<summary>If the value of certain variable is 1, you would like to use the value "one", otherwise, use "two". How would you do it?</summary>
<br>
<b> `{{ (certain_variable == 1) | ternary("one", "two") }}` </b>
</details>

<details>
<summary>The value of a certain variable you use is the string "True". You would like the value to be a boolean. How would you cast it?</summary>
<br>
<b> `{{ some_string_var | bool }}` </b>
</details>

<details>
<summary>You want to run Ansibleplaybook only on specific minor version of your OS, how would you achieve that?</summary>
<br>
<b> </b>
</details>

<details>
<summary>What the "become" directive used for in Ansible?</summary>
<br>
<b> The `become` directive is used to execute tasks with privilege escalation (e.g., as root). It's similar to using `sudo` in a shell. </b>
</details>

<details>
<summary>What are facts? How to see all the facts of a certain host?</summary>
<br>
<b> Facts are variables that are automatically discovered by Ansible from a managed node. They contain information about the system, such as network interfaces, operating system, and memory. To see all the facts of a certain host, you can use the `ansible -m setup` command. </b>
</details>

<details>
<summary>What would be the result of running the following task? How to fix it?
<pre>
- hosts: localhost
  tasks:
    - name: Install zlib
      package:
        name: zlib
        state: present
</pre>
</summary>
<br>
<b> The task will fail because it's trying to install a package on the local machine without the necessary privileges. To fix this, you need to add the `become: yes` directive to the task. </b>
</details>

<details>
<summary>Which Ansible best practices are you familiar with?. Name at least three</summary>
<br>
<b> - Use roles to organize your playbooks. - Use variables to make your playbooks more flexible. - Use version control to track changes to your playbooks. </b>
</details>

<details>
<summary>Explain the directory layout of an Ansible role</summary>
<br>
<b> A role is a set of tasks, handlers, variables, and templates that can be included in a playbook. The directory layout of a role is as follows: `defaults/` `files/` `handlers/` `meta/` `tasks/` `templates/` `vars/` </b>
</details>

<details>
<summary>What 'blocks' are used for in Ansible?</summary>
<br>
<b> Blocks are used to group tasks together. This can be useful for organizing your playbooks and for error handling. </b>
</details>

<details>
<summary>How do you handle errors in Ansible?</summary>
<br>
<b> You can use the `block` and `rescue` keywords to handle errors in Ansible. The `block` keyword is used to group tasks together, and the `rescue` keyword is used to specify a list of tasks to run if any of the tasks in the block fail. </b>
</details>

<details>
<summary>You would like to run a certain command if atask fails. How would you achieve that?</summary>
<br>
<b> You can use the `rescue` keyword to run a command if a task fails. For example:
<pre>
- hosts: all
  tasks:
    - block:
        - name: "Attempt to do something that might fail"
          command: /usr/bin/false
      rescue:
        - name: "Run this command if the task fails"
          command: /bin/echo "The task failed"
</pre>
</b>
</details>

<details>
<summary>Write a playbook to install ‘zlib’ and ‘vim’ on all hosts if the file ‘/tmp/mario’ exists on the system.</summary>
<br>
<b>
<pre>
---
- hosts: all
  vars:
    mario_file: /tmp/mario
    package_list:
      - 'zlib'
      - 'vim'

  tasks:
    - name: Check for mario file
      stat:
        path: "{{ mario_file }}"
      register: mario_f

    - name: Install zlib and vim if mario file exists
      become: "yes"
      package:
        name: "{{ item }}"
        state: present
      with_items: "{{ package_list }}"
      when: mario_f.stat.exists
</pre>
</b>
</details>

<details>
<summary>Write a single task that verifies all the files in files_list variable exist on the host</summary>
<br>
<b>
<pre>
- name: Ensure all files exist
  assert:
    that:
      - item.stat.exists
  loop: "{{ files_list }}"
</pre>
</b>
</details>

<details>
<summary>Write a playbook to deploy the file ‘/tmp/system_info’ on all hosts except for controllers group, with the following content</summary>
<br>
<b>
<pre>
I'm <HOSTNAME> and my operatingsystem is <OS>
</pre>
Replace <HOSTNAME> and <OS> with the actual data for the specific host you are running on

The playbook to deploy the system_info file
<pre>
---
- name: Deploy /tmp/system_info file
  hosts: all:!controllers

  tasks:
    - name: Deploy /tmp/system_info
      template:
        src: system_info.j2
        dest: /tmp/system_info
</pre>
The content of the system_info.j2 template
<pre>
I'm {{ ansible_hostname }} and my operating system is {{ ansible_distribution }
</pre>
</b>
</details>

<details>
<summary>The variable 'whoami' defined in the following places: * role defaults -> whoami: mario * extra vars (variables you pass to Ansible CLI with -e) -> whoami: toad * host facts -> whoami: luigi * inventory variables (doesn’t matter which type) -> whoami: browser According to variable precedence, which one will be used?</summary>
<br>
<b> The right answer is ‘toad’. Variable precedence is about how variables override each other when they set in different locations. If you didn’t experience it so far I’m sure at some point you will, which makes it a useful topic to be aware of. In the context of our question, the order will be extra vars (always override any other variable) -> host facts -> inventory variables -> role defaults (the weakest). Here is the order of precedence from least to greatest (the last listed variables winning prioritization): 1. command line values (eg “-uuser”) 2. role defaults [[1\]](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#id15) 3. inventory file or script group vars [[2\]](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#id16) 4. inventory group_vars/all [[3\]](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#id17) 5. playbook group_vars/all [[3\]](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#id17) 6. inventory group_vars/* [[3\]](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#id17) 7. playbook group_vars/* [[3\]](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#id17) 8. inventory file or script host vars [[2\]](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#id16) 9. inventory host_vars/* [[3\]](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#id17) 10. playbook host_vars/*[[3\]](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#id17) 11. host facts / cached set_facts [[4\]](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#id18) 12. play vars 13. play vars_prompt 14. play vars_files 15. role vars (defined in role/vars/main.yml) 16. block vars (only for tasks in block) 17. task vars (only for the task) 18. include_vars 19. set_facts / registered vars 20. role (and include_role) params 21. include params 22. extra vars (always win precedence) A full list can be found at [PlayBook Variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#ansible-variable-precedence) . Also, note there is a significant difference between Ansible 1.x and 2.x. </b>
</details>

<details>
<summary>For each of the following statements determine if it's true or false: * A module is a collection of tasks * It’s better to use shell or command instead of a specific module * Host facts override playvariables * A role might include the following: vars, meta, and handlers * Dynamic inventory is generated by extracting information from external sources * It’s a best practice to use indentation of 2 spaces instead of 4 * ‘notify’ used to trigger handlers * This “hosts: all:!controllers” means ‘run only on controllers group hosts</summary>
<br>
<b> </b>
</details>

<details>
<summary>Explain the Difference between Forks and Serial & Throttle.</summary>
<br>
<b> `Serial` is like running the playbook for each host in turn, waiting for completion of the complete playbook before moving on to the next host. `forks`=1 means run the first task in a play on one host before running the same task on the next host, so the first task will be run for each host before the next task is touched. Default fork is 5 in ansible.
<pre>
[defaults]
forks = 30
</pre>
<pre>
- hosts: webservers
  serial: 1
  tasks:
    - name: ...
</pre>
Ansible also supports `throttle` This keyword limits the number of workers up to the maximum setvia the forks setting or serial. This can be useful in restricting tasks that may be CPU-intensive or interact with a rate-limiting API
<pre>
tasks:
  - command: /path/to/cpu_intensive_command
    throttle: 1
</pre>
</b>
</details>

<details>
<summary>What is ansible-pull? How is it different from how ansible-playbook works?</summary>
<br>
<b> `ansible-pull` is a small script that pulls a playbook from a Git repository and then runs it. It's useful for a decentralized architecture where you don't have a central server to run `ansible-playbook`. </b>
</details>

<details>
<summary>What is Ansible Vault?</summary>
<br>
<b> Ansible Vault is a feature of Ansible that allows you to encrypt sensitive data, such as passwords and API keys, and store them in your playbook. </b>
</details>

<details>
<summary>Demonstrate each of the following with Ansible: * Conditionals * Loops </summary>
<br>
<b> **Conditionals**
<pre>
- hosts: all
  tasks:
    - name: "Install a package if it's a Debian-based system"
      package:
        name: "{{ item }}"
        state: present
      with_items:
        - vim
        - git
      when: ansible_os_family == "Debian"
</pre>
**Loops**
<pre>
- hosts: all
  tasks:
    - name: "Create a list of users"
      user:
        name: "{{ item }}"
        state: present
      with_items:
        - user1
        - user2
        - user3
</pre>
</b>
</details>

<details>
<summary>What are filters? Do you have experience with writing filters?</summary>
<br>
<b> Filters are a way of transforming data in Ansible. They are used in templates and playbooks to manipulate variables. I have experience with writing custom filters in Python. </b>
</details>

<details>
<summary>Write a filter to capitalize a string</summary>
<br>
<b>
<pre>
def cap(self, string):
    return string.capitalize()
</pre>
</b>
</details>

<details>
<summary>You would like to run a task only if previous task changed anything. How would you achieve that?</summary>
<br>
<b> You can use the `when` conditional with the `changed` variable. For example:
<pre>
- hosts: all
  tasks:
    - name: "Run a command"
      command: /usr/bin/something
      register: result
    - name: "Run this task only if the previous task changed something"
      command: /usr/bin/something_else
      when: result.changed
</pre>
</b>
</details>

<details>
<summary>What are callback plugins?What can you achieve by using callback plugins?</summary>
<br>
<b> Callback plugins are a way to extend Ansible's functionality. They are executed at certain points during a playbook run, such as when a task starts or finishes. You can use callback plugins to do things like send notifications, log data to a file, or integrate with other tools. </b>
</details>

<details>
<summary>What is the difference between `include_task` and `import_task`?</summary>
<br>
<b> `import_task` is static and is processed at playbook parsing time. `include_task` is dynamic and is processed during the execution of the playbook. </b>
</details>

<details>
<summary>File '/tmp/exercise' includes the following content
<pre>
Goku = 9001
Vegeta = 5200
Trunks = 6000
Gotenks = 32
</pre>
With one task, switch the content to:
<pre>
Goku = 9001
Vegeta = 250
Trunks = 40
Gotenks = 32
</pre>
</summary>
<br>
<b>
<pre>
- name: Change saiyans levels
  lineinfile:
    dest: /tmp/exercise
    regexp: "{{ item.regexp }}"
    line: "{{ item.line }}"
  with_items:
    - { regexp: '^Vegeta', line: 'Vegeta = 250' }
    - { regexp: '^Trunks', line: 'Trunks = 40' }
    ...
</pre>
</b>
</details>

<details>
<summary>True or False? By default, Ansible will execute all the tasks in play on a single host before proceeding to the next host</summary>
<br>
<b> False. Ansible will execute a single task on all hosts before moving to the next task in a play. As for today, it uses 5 forks by default.<br> This behavior is described as "strategy" in Ansible and it's configurable. </b>
</details>

<details>
<summary>What is a "strategy" in Ansible? What is the default strategy?</summary>
<br>
<b> A strategy in Ansible describes how Ansible will execute the different tasks on the hosts. By default Ansible is using the "Linear strategy" which defines that each task will run on all hosts before proceeding to the next task. </b>
</details>

<details>
<summary>What strategies are you familiar with in Ansible?</summary>
<br>
<b> - Linear: the default strategy in Ansible. Run each task on all hosts before proceeding. - Free: For each host, run all the tasks until the end of the play as soon as possible -Debug: Run tasks in an interactive way </b>
</details>

<details>
<summary>What the <code>serial</code> keyword is used for?</summary>
<br>
<b> It's used to specify the number (or percentage) of hosts to run the full play on, before moving to next number of hosts in the group. For example:
<pre>
- name: Some play
  hosts: databases
  serial: 4
</pre>
If your group has 8 hosts. It will run the whole play on 4 hosts and then the same play on another 4 hosts. </b>
</details>

<details>
<summary>How do you test your Ansible based projects?</summary>
<br>
<b> </b>
</details>

<details>
<summary>What is Molecule? How does it works?</summary>
<br>
<b> It's used to rapidy develop and test Ansbile roles. Molecule can be used to test Ansible roles against a varaitey of Linux Distros at the same time. This testing ability helps instill confidence of the automation today and as time go on while a role is maintined. </b>
</details>

<details>
<summary>You run Ansible tests and you get "idempotence test failed". What does it mean? Why idempotence is important?</summary>
<br>
<b> </b>
</details>

<details>
<summary>How to find out the data type of a certain variable in one of the playbooks?</summary>
<br>
<b> "{{ some_var | type_debug }}" </b>
</details>

<details>
<summary>What are collections in Ansible?</summary>
<br>
<b> Ansible Collections are a way to package and distribute modules, roles, plugins, and documentation in a structured format. They help organize and distribute automation code efficiently, especially for complex environments. </b>
</details>

<details>
<summary>Why Use Ansible Collections?</summary>
<br>
<b> - Modular and reusable components - Simplifies management of custom and third-party modules - Provides a standardized way to distribute automation content - Helps in version control and dependency management </b>
</details>

## Exercises

|Name|Topic|Objective & Instructions|Solution|Comments|
|--------|--------|------|----|----|
| My First Task | Tasks | [Exercise](my_first_task.md) | [Solution](solutions/my_first_task.md) |
| Upgrade and Update Task | Tasks | [Exercise](update_upgrade_task.md) | [Solution](solutions/update_upgrade_task.md) |
| My First Playbook | Playbooks | [Exercise](my_first_playbook.md) | [Solution](solutions/my_first_playbook.md) |

## Additional Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [Awesome Ansible](https://github.com/ansible-community/awesome-ansible)